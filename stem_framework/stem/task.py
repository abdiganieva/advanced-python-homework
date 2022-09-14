"""
Pull data flow model is implemented in DataForge by workplaces and tasks. The task execution consists of three steps, namely:
	1) Task model (the system calculates an acyclic dependency graph of tasks and data).
	2) Lazy computation model (a ’Goal’ object is created for each specific computation).
	3) Computation (when the top level goal is triggered, it invokes computation of all goals in chain behind it).
"""
