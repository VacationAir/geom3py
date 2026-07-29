from ..geometry.vector import Vector

def linsys_solve(A, b, tol=1e-10):
    """
    Solves a linear system of equations using the Gauss-Jordan method.

    The method supports square, overdetermined and
    underdetermined linear systems of equations.

    Parameters
    ----------
    A : list[list[float]]
        Coefficient matrix.
    b : list[float]
        Right-hand side of the linear system of equations.
    tol : float, optional
        Tolerance for numerical comparisons.

    Returns
    -------
    list[float] or None
        A solution of the linear system of equations.
        If there are infinitely many solutions, free variables
        are set to 0.
        If no solution exists, None is returned.
    """

    # Create augmented matrix
    matrix = [
        list(map(float, row)) + [float(value)]
        for row, value in zip(A, b)
    ]

    m = len(matrix)
    n = len(A[0])

    pivot_row = 0
    pivot_columns = []

    # Gauss-Jordan
    for column in range(n):

        # Find pivot
        pivot = None
        max_value = tol

        for row in range(pivot_row, m):
            if abs(matrix[row][column]) > max_value:
                max_value = abs(matrix[row][column])
                pivot = row

        if pivot is None:
            continue

        # Swap rows
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row]
        )

        # Normalize pivot
        pivot_value = matrix[pivot_row][column]

        for j in range(column, n + 1):
            matrix[pivot_row][j] /= pivot_value

        # Eliminate all other rows
        for row in range(m):

            if row == pivot_row:
                continue

            factor = matrix[row][column]

            if abs(factor) < tol:
                continue

            for j in range(column, n + 1):
                matrix[row][j] -= factor * matrix[pivot_row][j]

        pivot_columns.append(column)
        pivot_row += 1

        if pivot_row == m:
            break

    # Remove numerical noise
    for i in range(m):
        for j in range(n + 1):
            if abs(matrix[i][j]) < tol:
                matrix[i][j] = 0.0

    # Check for contradiction
    for row in matrix:
        if all(abs(row[j]) < tol for j in range(n)) and abs(row[-1]) > tol:
            return None

    # Construct a solution
    solution = [0.0] * n

    for i in range(m):

        pivot = None

        for j in range(n):
            if abs(matrix[i][j] - 1.0) < tol:
                pivot = j
                break

        if pivot is not None:
            solution[pivot] = matrix[i][-1]

    return solution

def close(a, b, tol=1e-8):
    if isinstance(a, Vector):
        if isinstance(b, Vector):
            return abs((a - b).magnitude()) < tol
        
        elif isinstance(b, (int, float)):
            return abs(a.magnitude() - b) < tol
        
    elif isinstance(b, Vector):
        if isinstance(a, (int, float)):
            return abs(a - b.magnitude()) < tol
        
    elif isinstance(a, list):
        if isinstance(b, (int, float)):
            return all(abs(x - b) < tol for x in a)
        
        elif isinstance(b, list):
            if len(a) != len(b):
                return False
            return all(abs(a[i] - b[i]) < tol for i in range(len(a)))
        
    return abs(a - b) < tol