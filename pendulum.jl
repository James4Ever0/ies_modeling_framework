# create single pendulum model

using DifferentialEquations

# using Plots

l = 1.0                             # length [m]
m = 1.0                             # mass [kg]
g = 9.81                            # gravitational acceleration [m/s²]

# (state_derivatives, states, external_control_function, time)
function pendulum!(du,u,p,t)
    du[1] = u[2]                    # θ'(t) = ω(t)
    du[2] = -3g/(2l)*sin(u[1]) + 3/(m*l^2)*p(t) # ω'(t) = -3g/(2l) sin θ(t) + 3/(ml^2)M(t)
end

θ₀ = 0.01                           # initial angular deflection [rad]
ω₀ = 0.0                            # initial angular velocity [rad/s]
u₀ = [θ₀, ω₀]                       # initial state vector
tspan = (0.0,10.0)                  # time interval

M = t->0.1sin(t)                    # external torque [Nm], function

# (ode_function, initial_states, timespan, )
prob = ODEProblem(pendulum!,u₀,tspan,M)


sol = solve(prob)

# Plots.gr()
# Plots.PyPlotBackend()
# Plots.plot(sol,linewidth=2,xaxis="t",label=["θ [rad]" "ω [rad/s]"],layout=(2,1))

# println(u)
states = sol.u
states_matrix = mapreduce(permutedims, vcat,states)

angular_deflections = states_matrix[:,1]
angular_velocities = states_matrix[:,2]
