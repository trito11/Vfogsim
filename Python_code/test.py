import numpy as np
import gurobipy as gp
from gurobipy import GRB

def intlinprog_gurobi(f, intcon, A, b, Aeq=None, beq=None, lb=None, ub=None):
    # Xác định số lượng biến
    if A is not None:
        n = A.shape[1]
    elif Aeq is not None:
        n = Aeq.shape[1]
    else:
        raise ValueError('No linear constraints specified')

    # Chuyển đổi ma trận ràng buộc sang định dạng tuplelist
    A = gp.tuplelist(A) if A is not None else None
    Aeq = gp.tuplelist(Aeq) if Aeq is not None else None

    # Tạo mô hình Gurobi
    model = gp.Model()

    # Thiết lập loại biến
    vtype = ['C'] * n
    for i in intcon:
        vtype[i] = 'I'

    # Thêm biến vào mô hình
    x = model.addVars(n, vtype=vtype,name="x")
    # Thiết lập hàm mục tiêu
    model.setObjective(gp.quicksum(f[j] * x[j] for j in range(n)), GRB.MINIMIZE)

    # Thêm ràng buộc không bằng nhau
    if A is not None:
        for i in range(len(A)):
            model.addConstr(gp.quicksum(A[i][j] * x[j] for j in range(n)) <= b[i])

    # Thêm ràng buộc bằng nhau
    if Aeq is not None:
        for i in range(len(Aeq)):
            model.addConstr(gp.quicksum(Aeq[i][j] * x[j] for j in range(n)) == beq[i])

    # Thiết lập giới hạn dưới và giới hạn trên
    if lb is not None:
        model.setAttr('LB', x, lb)
    if ub is not None:
        model.setAttr('UB', x, ub)

    # Thiết lập tham số của trình giải
    model.setParam('OutputFlag', 0)
    model.setParam('TimeLimit', 1800)

    # Tối ưu hóa mô hình
    model.optimize()

    # Trích xuất kết quả tối ưu hóa
    if model.status == GRB.OPTIMAL:
        print('Optimal solution:')
        for v in model.getVars():
            print(f'{v.varName} = {v.x}')
        print(f'Obj: {model.objVal}')
    else:
        print('No solution')

    

def generate_random_data(m, n, n_eq=None, n_intcon=None):
    # Tạo dữ liệu ngẫu nhiên cho các tham số
    f = np.random.rand(n)
    A = np.random.rand(m, n)
    b = np.random.rand(m)
    Aeq = None
    beq = None
    if n_eq:
        Aeq = np.random.rand(n_eq, n)
        beq = np.random.rand(n_eq)
    lb = np.random.rand(n)
    ub = np.random.rand(n)
    intcon = None
    if n_intcon:
        intcon = np.random.choice(range(n), n_intcon, replace=False)
    return f, intcon, A, b, Aeq, beq, lb, ub

# Số lượng biến và ràng buộc
m = 20  # Số lượng ràng buộc
n = 15   # Số lượng biến
n_eq = 2  # Số lượng ràng buộc bằng nhau
n_intcon = 5  # Số lượng biến nguyên

# Sinh dữ liệu ngẫu nhiên
f, intcon, A, b, Aeq, beq, lb, ub = generate_random_data(m, n, n_eq, n_intcon)

# In các tham số đã sinh
print("f:", f)
print("intcon:", intcon)
print("A:", A)
print("b:", b)
print("Aeq:", Aeq)
print("beq:", beq)
print("lb:", lb)
print("ub:", ub)

intlinprog_gurobi(f, intcon, A, b, None, None, lb, ub)
# In ra giá trị của biến tối ưu và giá trị tối ưu của hàm mục tiêu
