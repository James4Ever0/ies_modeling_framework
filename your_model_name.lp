\* Source Pyomo model name=unknown *\

min 
obj:
+1 变量x

s.t.

c_u_expr_0_:
-1 变量y
+1 变量z
<= 0

c_l_expr_1_:
+1 变量y
>= 20

c_u_expr_2_:
+1 变量y
<= 10

c_l_expr_3_:
+1 变量h
>= 20

c_u_expr_4_:
+1 变量h
<= 10

c_u_expr_5_:
+1 变量z
<= 0

c_l_expr_6_:
+1 变量z
>= -10

c_u_expr_7_:
+0.5 变量h
+1 变量x
+0.5 变量y
<= 100

c_u_expr_8_:
+0.5 变量h
-1 变量x
+0.5 变量y
-1 变量z
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
    -inf <= 变量x <= +inf
    -inf <= 变量y <= +inf
    -inf <= 变量z <= +inf
    -inf <= 变量h <= +inf
end
