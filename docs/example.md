# Utils Documentation Template

## Function: `generic_function`
```python
generic_function(param1, param2)
```

### Description
Performs a generic operation on the given parameters.

### Notes
- Ensure input parameters are of the correct types to avoid runtime errors.

### Arguments
- **`param1`** (`Union[float, int]`):  
    The first parameter for the operation.  
- **`param2`** (`Union[float, int]`):  
    The second parameter for the operation.

### Returns
- **`float`**:  
    The result of the operation performed on the parameters.

### Raises
- **`ValueError`**:  
    Raised when either argument is not a number.

### Example Usage

<!-- tabs:start -->

#### **Example 1**
```python
result = generic_function(10, 20)
print(f"Result: {result}")
```
**Expected Output:**
```
Result: 30.0
```

#### **Example 2**
```python
try:
        result = generic_function("10", 20)
except ValueError as e:
        print(f"Error: {e}")
```
**Expected Output:**
```
Error: Both arguments must be numbers.
```

<!-- tabs:end -->

---

## Class: `GenericProcessor`
```python
processor = GenericProcessor()
```

A class for processing data with user-defined rules.

### Methods

#### `add_rule`
```python
add_rule(rule_func, description)
```

Adds a processing rule to the class.

- **Parameters**:
    - **`rule_func`** (`callable`): Function defining the processing rule.
    - **`description`** (`str`): A brief description of the rule.

- **Raises**:
    - **`ValueError`**: If `rule_func` is not callable.
    - **`TypeError`**: If `description` is not a string.

---

#### `apply_rules`
```python
apply_rules(data)
```

Processes the input data using all added rules.

- **Parameters**:
    - **`data`** (`Any`): The input data to be processed.

- **Returns**:
    - **`processed_data`** (`Any`): The data after applying all rules.
    - **`violations`** (`list[str]`): List of violations encountered during processing.

- **Raises**:
    - **`Exception`**: Raised if an error occurs while applying a rule.

### Example Usage

```python
from mylibrary.processors import GenericProcessor

def rule_func(data):
        return data > 0

processor = GenericProcessor()
processor.add_rule(rule_func, "Check if data is positive")

data = [-1, 0, 1, 2]
processed, violations = processor.apply_rules(data)

print("Processed Data:", processed)
print("Violations:", violations)
```
**Expected Output:**
```
Processed Data: [1, 2]
Violations: ['Rule violated: Check if data is positive']
```
