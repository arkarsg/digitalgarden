import builtins
from random import randint
from typing import Any
from typing import Callable
from typing import List

'''
Implementing a Golang-like coroutines scheduler API

Goroutines will be modelled as coroutines using a queue of functions
'''

'''
Channel class
'''
class Channel:
    def __init__(self):
        self.closed: bool = False
        self.waiting_to_send: WaitingQueue = WaitingQueue()
        self.waiting_to_recv: WaitingQueue = WaitingQueue()

'''
Waiting Queue class

Supports enqueueing and dequeing elements
`total` is a class variable
'''
class WaitingQueue(list):
    total: int = 0

    def enqueue(self, x: Any) -> None:
        WaitingQueue.total += 1
        self.append(x)

    def dequeue(self, x: Any = None) -> Any:
        if x is None:
            x = self.pop(0)
            WaitingQueue.total -= 1
        else:
            index = self.index(x)
            if index is not None:
                self.pop(index)
                WaitingQueue.total -= 1
        return x

'''
Golang-like coroutines scheduler API
'''
default = object() # To use in select
execution_queue = []

def go(callback: Callable) -> None:
    '''
    Enqueues a function for execution

    Params
        callback: function for execution
    '''
    if callback:
        execution_queue.append(callback)

def run():
    '''
    Dequeue a function and run it until there are no functions left
    '''
    while execution_queue:
        func = execution_queue.pop(0)
        func()

    if WaitingQueue.total > 0:
        raise Exception("Fatal error: all goroutines are asleep - deadlock")

def make() -> Channel:
    return Channel()

def len(channel) -> int:
    return 0 # Unbuffered channel

def cap(channel) -> int:
    return 0 # Unbuffered channel

def send(channel: Channel, value: Any, callback: Callable):
    '''
    Communication blocks until send can proceed.
    - A send on an unbuffered channel can proceed if a receiver is ready
    - A send on a closed channel proceeds by causing a run-time panic.
    - A send on a nil channel blocks forever
    '''
    if channel is None:
        WaitingQueue.total += 1
        return

    if channel.closed:
        raise Exception("Panic: send on closed channel")

    if channel.waiting_to_recv:
        # Receiver is ready, send can proceed
        receiver = channel.waiting_to_recv.dequeue()
        go(callback)
        go(lambda: receiver(value, True))
        return

    channel.waiting_to_send.enqueue((value, callback))

def recv(channel: Channel, callback: Callable) -> None:
    '''
    Takes in a channel and a callback.
    Tries to find a matching send operation.
    If none is found, we push the callback function onto the `waiting_to_recv` queue
    '''
    if channel is None:
        WaitingQueue.total += 1
        return

    if channel.waiting_to_send:
        # If there is anything waiting on the send queue, receive it
        value, sender_callback = channel.waiting_to_send.dequeue()
        go(lambda: callback(value, True))
        go(sender_callback)
        return

    if channel.closed:
        go(lambda: callback(None, False))
        return

    channel.waiting_to_recv.enqueue(callback)

def close(channel: Channel):
    if channel.closed:
        raise Exception("close of a closed channel")

    channel.closed = True

    # Complete senders
    while channel.waiting_to_send:
        value, callback = channel.waiting_to_send.dequeue()
        send(channel, value, callback)

    # Complete receivers
    while channel.waiting_to_recv:
        callback = channel.waiting_to_recv.dequeue()
        recv(channel, callback)

def select(cases, callback: Callable = None):
    '''
    At least one of the cases is able to proceed: Choose one at random and execute
    None of the cases are able to proceed, but has default case: Execute default
    None of the cases are able to proceed, no default case:
        - enqueue waiting callbacks into each of the channels for sending/ recving
        - When one of those callbacks is chosen, remove all others to ensure that
          only one of the cases proceed
    '''
    def is_ready(case):
        if case[0] == send:
            return case[1].closed or case[1].waiting_to_recv
        elif case[0] == recv:
            return case[1].closed or case[1].waiting_to_send
        elif case[0] == default:
            return False


    ready = [case for case in cases if is_ready(case)]
    if ready:
        case = ready[randint(0, builtins.len(ready) - 1)]
        if case[0] == send:
            send(case[1], case[2], case[3])
        elif case[0] == recv:
            recv(case[1], case[2])
        go(callback)
        return

    defaults = [case for case in cases if case[0] == default]
    if defaults:
        defaults[0]()
        go(callback)
        return


    wrapped = []
    def cleanup():
        for case in wrapped:
            if case[0] == send:
                case[1].waiting_to_send.dequeue((case[2], case[3]))
            elif case[0] == recv:
                case[1].waiting_to_recv.dequeue(case[2])
        go(callback)

    for case in cases:
        if case[0] == send:
            new_case = (case[0], case[1], case[2], lambda: (cleanup(), case[3]()))
            case[1].waiting_to_send.enqueue((new_case[2], new_case[3]))
            wrapped.append(new_case)
        elif case[0] == recv:
            new_case = (case[0], case[1], lambda value, ok: (cleanup(), case[2](value, ok)))
            case[1].waiting_to_recv.enqueue(new_case[2])
            wrapped.append(new_case)

'''
Concurrent merge sort
'''
def merge(l: List, r: List) -> List:
    m = []
    while builtins.len(l) > 0 or builtins.len(r) > 0:
        if builtins.len(l) == 0:
            m.append(r[0])
            r = r[1:]
        elif builtins.len(r) == 0:
            m.append(l[0])
            l = l[1:]
        elif l[0] <= r[0]:
            m.append(l[0])
            l = l[1:]
        else:
            m.append(r[0])
            r = r[1:]
    return m


def concurrent_merge_sort(series_of_numbers: List, callback: Callable):
    n = builtins.len(series_of_numbers)

    if n <= 1:
        callback(series_of_numbers)
    else:
        left_channel, right_channel = make(), make()

        go(lambda: concurrent_merge_sort(
                        series_of_numbers[: n // 2],
                        lambda left: send(left_channel, left, lambda: None)
        ))

        go(lambda: concurrent_merge_sort(
                        series_of_numbers[n // 2:],
                        lambda right: send(right_channel, right, lambda: None)
        ))

        recv(left_channel, lambda left, _:
            recv(right_channel, lambda right, _:
                    callback(merge(left, right))))

def test_concurrent_merge_sort():
    test_input = [2, 3, 1, 5, 4]
    expected_result = [1, 2, 3, 4, 5]

    def callback(result):
        print(result)
        assert result == expected_result

    concurrent_merge_sort(test_input, callback)
    run()