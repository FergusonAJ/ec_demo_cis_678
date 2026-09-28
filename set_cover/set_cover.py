import copy
import sys
import random

class SetCoverSolver:
  def __init__(self, people, pop_size, mut_rate, num_elites = 0):
    self.people = copy.deepcopy(people)
    self.num_skills = len(self.people[0])
    for idx, person in enumerate(self.people):
      if len(person) != self.num_skills:
        print('Error! Malformed list given to SetCoverSolver')
        print(f'First person had {self.num_skills} skills, while person at index {idx} has {len(person)}')
        print('Terminating')
        sys.exit(1)
    self.pop_size = pop_size
    self.mut_rate = mut_rate
    self.num_elites = num_elites
    self.pop = []
    self.generate_population()

  def generate_solution(self):
    sol = [False] * len(self.people)
    for idx in range(len(self.people)):
      if random.uniform(0, 1) < 0.5:
        sol[idx] = True
    return sol

  def generate_population(self):
    self.pop = []
    for idx in range(self.pop_size):
      self.pop.append(self.generate_solution())

  def boolean_list_to_string(self, L):
    s = '['
    for b in L:
      if b:
        s += '1'
      else:
        s += '0'
    s += ']'
    return s

  def print_solution(self, sol, verbose = False):
    sol_str = self.boolean_list_to_string(sol)
    task_str = self.boolean_list_to_string(self.get_task_coverage(sol))
    fitness_str = str(round(self.get_solution_fitness(sol), 2))
    print(f'{sol_str} -> {task_str} = {fitness_str}')

  def print_population(self, pop = None, verbose = False):
    if pop is None:
      pop = self.pop
    for x in pop:
      self.print_solution(x, verbose)

  def get_task_coverage(self, sol):
    tasks_covered = [False] * self.num_skills
    for person_idx in range(len(sol)):
      # If this person is included
      if sol[person_idx]:
        for task_idx, task_val in enumerate(self.people[person_idx]):
          if task_val:
            tasks_covered[task_idx] = True
    return tasks_covered

  def get_solution_fitness(self, sol):
    tasks_covered = self.get_task_coverage(sol)
    num_skills_covered = sum(tasks_covered)
    frac = num_skills_covered / self.num_skills
    if frac >= 1.0:
      score = 100 - 80 * (sum(sol) / len(self.people))
    else:
      score = frac
    return score

  def select(self, num_orgs):
    total_fitness = 0
    cumulative_fitnesses = []
    max_fitness = None
    max_fitness_orgs = []
    for org in self.pop:
      org_fitness = self.get_solution_fitness(org)
      total_fitness += org_fitness
      cumulative_fitnesses.append(total_fitness)
      if max_fitness is None or org_fitness > max_fitness:
        max_fitness = org_fitness
        max_fitness_orgs = [org]
      elif org_fitness == max_fitness:
        max_fitness_orgs.append(org)
    selected_orgs = []
    if self.num_elites > 0:
      selected_orgs += random.choices(max_fitness_orgs, k = self.num_elites)
    #print('Elite orgs:')
    #self.print_population(selected_orgs, True)
    for i in range(num_orgs - self.num_elites):
      random_val = random.uniform(0, total_fitness)
      for org_idx, org in enumerate(self.pop):
        if random_val < cumulative_fitnesses[org_idx]:
          selected_orgs.append(copy.deepcopy(org))
          break
    return selected_orgs

  def mutate(self, sol):
    offspring = copy.deepcopy(sol)
    for idx in range(len(sol)):
      if random.uniform(0, 1) < self.mut_rate:
        offspring[idx] = not offspring[idx]
    return offspring

  def run(self, num_gens, verbose = False):
    for gen_idx in range(num_gens):
      print(f'==== Gen {gen_idx} ====')
      parents = self.select(self.pop_size)
      self.pop = []
      for idx, parent in enumerate(parents):
        if idx >= self.num_elites:
          self.pop.append(self.mutate(parent))
        else:
          self.pop.append(parent)
      max_fitness = None
      avg_fitness = 0
      for org in self.pop:
        fitness = self.get_solution_fitness(org)
        if max_fitness is None or fitness > max_fitness: 
          max_fitness = fitness
        avg_fitness += fitness
      avg_fitness /= len(self.pop)
      print(f'Max fitness: {round(max_fitness, 2)}, Avg. fitness: {round(avg_fitness, 2)}')
      if verbose:
        self.print_population(verbose = True)



if __name__ == '__main__':
  generate_people = False
  if not generate_people:
    people = [
        [True, False, False, False], 
        [False, True, False, False], 
        [False, False, True, False], 
        [False, False, False, True], 
        [True, True, False, False], 
        [False, True, False, True], 
        [False, False, True, True]]
  else:
    num_people = 100
    num_tasks = 50
    task_prob = 0.05
    people = []
    for i in range(num_people):
      tasks  = []
      for j in range(num_tasks):
        if random.uniform(0, 1) < task_prob:
          tasks.append(True)
        else:
          tasks.append(False)
      people.append(tasks)

  solver = SetCoverSolver(people, pop_size = 100, mut_rate = 0.05, num_elites = 3)
  solver.run(100)
  solver.print_population(verbose = True)

