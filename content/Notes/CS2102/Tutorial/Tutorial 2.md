>[!note]- For reference
>![[Data Modelling#Entity relationship diagrams]]

#### Question 1

- Strong entity types : CUSTOMER, ACCOUNT, LOAN
- Weak entity type : BANK_BRANCH
	- Identifying relationship : BRANCHES with BANK
	- Partial identifier : Branch_no
	- Complete identifier : BANK Code + Branch_no
- Participation in L_C:
	- total in LOAN *every LOAN is expected to have at least one CUSTOMER*
	- partial in CUSTOMER *CUSTOMER may or may not have LOANS L_C*
	- Possible since it’s a ==many-to-many== relationship 
- Yes
- Yes
- CUSTOMER has a partial constraint on A_C

---

#### Question 1B
- BANK_BRANCH(<u>Branch_no</u>, Addr, <u>Code</u>)
- Bank_code, Branch_no
	- Customer SSN should not be included because an account can be owned by multiple customers.
- L_C(Loan_no, Ssn)
- By incorporating the foreign key (Branch_no, Bank_code) into LOAN
- Under ACCOUNT
>[!caution]
>Attach Opening_date to A_C

---

#### Question 2


---

#### Question 3

- True, ACTOR has a total participation in PERFORMS_IN
- Maybe, ACTOR can PERFORM_IN N movies
- True
- True, MOVIE can have [0, 2] LEAD ROLE
- False, DIRECTOR has an optional participation to ALSO_A_DIRECTOR
- Maybe
- Maybe
- Maybe
- False
- True
- Maybe

---