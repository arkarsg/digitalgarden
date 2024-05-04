# Sorting Algorithms
- **Stable sorting** : Two objects with equal keys appear in the same order in sorted output as they appear in the input array

## Bubble sort
>[!note] Key idea
>Repeatedly swap adjacent elements that are out of order until there are no swaps in *an iteration*, or after $n$ iteration

Suppose there is an unsorted array of $n$ elements. Each pass *bubbles* an element to the correct position.
- Total number of passes : $n-1$
- Total number of comparisons : $n * \frac{n-1}{2}$

After $i$ iterations, largest $i$ elements are correctly sorted in the final $i$ positions of the array

**Bubble sort is stable**
Suppose an array, $A = [2, 2, 1]$
- By the Bubble sort algorithm, the adjacent elements $[2, 2]$ will never be swapped by the comparison

```python
arr = [6, 0, 3, 5]

def bubble_sort(arr):
	n = len(arr)
	for i in range(n):
		swapped = False
		for j in range(0, n - i - 1):
			if arr[j] > arr[j + 1]:
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
				swapped = True
		if not swapped:
			break

bubble_sort(arr)
print(arr)
```

### Complexity
- **Best case** : sorted array → $O(n)$ comparisons
- Otherwise, $O(n^2)$ comparisons
- Array is sorted in-place → $O(1)$

---

## Selection sort
>[!note] Key idea
>Maintain a sorted prefix. Repeatedly find the smallest element in the *unsorted remainder* and swaps it with the first element in the *unsorted remainder*. The sorted prefix and the first element of the *unsorted remainder* then becomes the new sorted prefix

After $i$ iterations, the smallest $i$ elements are correctly sorted in the final $i$ positions of the array

**Selection sort is unstable**
Suppose an array, $A = [2, 2, 1]$
- By Selection sort algorithm, the adjacent elements $[2, 2]$ will no longer be in the same order after the array has been sorted

```python
arr = [6, 0, 3, 5]

def selection_sort(arr):
	n = len(arr)
	for i in range(n - 1):
		min_index_so_far = i
		for j in range(i + 1, n):
			if arr[min_index_so_far] > arr[j]:
				min_index_so_far = j
		arr[i], arr[min_index_so_far] = arr[min_index_so_far], arr[i]

selection_sort(arr)
print(arr)
```

### Complexity
- $O(n^2)$ comparisons

---

## Insertion sort
>[!note] Key idea
>Maintain a sorted prefix. Repeatedly insert unsorted elements into the correct place in the sorted prefix. in other words, we are building a sorted array one element at a time

After iteration $i$, the first $i$ items are in sorted order

**Insertion sort is stable**

```python
arr = [6, 0, 3, 5]

def insertion_sort(arr):
	n = len(arr)
	# assume the first element to be sorted
	for i in range(1, n):
		elem = arr[i]
		j = i - 1
		while j >= 0 and elem < arr[j]:
			arr[j + 1] = arr[j]
			j -= 1
		arr[j + 1] = elem

insertion_sort(arr)
print(arr)
```

### Complexity
- **Best case** : $O(n)$
- **Worst case** : $O(n^2)$

---

## Merge sort
>[!note] Key idea
>Refer to [Divide and Conquer](Divide%20and%20Conquer.md)

---
