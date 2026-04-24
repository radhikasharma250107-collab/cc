from collections import defaultdict, deque


# ---------------- TASK CLASS ----------------

class Task:
    def __init__(self, name, priority, deadline, duration=1):
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.duration = duration

    def __repr__(self):
        return f"Task({self.name}, priority={self.priority}, deadline={self.deadline}, duration={self.duration})"


# ---------------- TASK SCHEDULER ----------------

class TaskScheduler:

    def __init__(self):
        self.tasks = {}
        self.adj = defaultdict(list)
        self.in_degree = defaultdict(int)

    def add_task(self, name, priority, deadline, duration=1):
        if name in self.tasks:
            print(f"Task '{name}' already exists.")
            return
        self.tasks[name] = Task(name, priority, deadline, duration)
        self.in_degree[name]
        print(f"Added: {name}")

    def add_dependency(self, before, after):
        if before not in self.tasks or after not in self.tasks:
            print("Task not found.")
            return
        self.adj[before].append(after)
        self.in_degree[after] += 1
        print(f"{before} -> {after}")

    def print_graph(self):
        print("\nDEPENDENCY GRAPH")
        print("-" * 40)
        for task in self.tasks:
            print(f"{task} -> {self.adj[task]}")
        print()

    # -------- Cycle Detection (DFS) --------

    def has_cycle(self):
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {t: WHITE for t in self.tasks}

        def dfs(node):
            color[node] = GRAY
            for nei in self.adj[node]:
                if color[nei] == GRAY:
                    return True
                if color[nei] == WHITE and dfs(nei):
                    return True
            color[node] = BLACK
            return False

        for t in self.tasks:
            if color[t] == WHITE:
                if dfs(t):
                    return True
        return False

    # -------- Topological Sort --------

    def topological_sort(self):
        in_deg = dict(self.in_degree)

        queue = deque(sorted(
            [t for t in self.tasks if in_deg[t] == 0],
            key=lambda x: (self.tasks[x].priority, self.tasks[x].deadline)
        ))

        order = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for nei in self.adj[current]:
                in_deg[nei] -= 1
                if in_deg[nei] == 0:
                    queue.append(nei)
                    queue = deque(sorted(
                        list(queue),
                        key=lambda x: (self.tasks[x].priority, self.tasks[x].deadline)
                    ))

        if len(order) != len(self.tasks):
            print("Cycle detected. Cannot schedule.")
            return None

        print("\nExecution Order:")
        print(" -> ".join(order))
        return order

    # -------- Timeline --------

    def build_schedule(self):
        order = self.topological_sort()
        if not order:
            return

        print("\nEXECUTION TIMELINE")
        print("-" * 50)
        print(f"{'Task':<25} {'Start':>5} {'End':>5} {'Status'}")
        print("-" * 50)

        finish = {}

        for task_name in order:
            task = self.tasks[task_name]

            prereq_end = [
                finish[p] for p in finish if task_name in self.adj[p]
            ]

            start = max(prereq_end, default=0)
            end = start + task.duration
            finish[task_name] = end

            status = "ON TIME" if end <= task.deadline else "LATE"

            print(f"{task_name:<25} {start:>5} {end:>5} {status}")

        print("\nTotal Time:", max(finish.values()))


# ---------------- DEMO ----------------

def run_demo():
    s = TaskScheduler()

    print("\nSTEP 1: ADD TASKS")
    s.add_task("Install OS", 1, 2, 2)
    s.add_task("Install Python", 2, 4, 1)
    s.add_task("Setup Database", 2, 6, 2)
    s.add_task("Write Backend", 3, 10, 3)
    s.add_task("Write Frontend", 3, 10, 3)
    s.add_task("Connect", 2, 14, 1)
    s.add_task("Testing", 1, 16, 2)
    s.add_task("Deploy", 1, 20, 1)

    print("\nSTEP 2: ADD DEPENDENCIES")
    s.add_dependency("Install OS", "Install Python")
    s.add_dependency("Install OS", "Setup Database")
    s.add_dependency("Install Python", "Write Backend")
    s.add_dependency("Install Python", "Write Frontend")
    s.add_dependency("Setup Database", "Write Backend")
    s.add_dependency("Write Backend", "Connect")
    s.add_dependency("Write Frontend", "Connect")
    s.add_dependency("Connect", "Testing")
    s.add_dependency("Testing", "Deploy")

    s.print_graph()

    print("STEP 3: CYCLE CHECK")
    if s.has_cycle():
        print("Cycle detected!")
        return
    print("No cycle found.")

    print("\nSTEP 4: SCHEDULING")
    s.build_schedule()


if __name__ == "__main__":
    run_demo()