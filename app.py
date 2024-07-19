import pandas as pd
from deap import base, creator, tools, algorithms
import random
from flask import Flask, render_template, request, jsonify

# Dataset
data = {
    'Tanggal': ['9-Sep-23', '9-Sep-23', '9-Sep-23', '9-Sep-23', '30-Sep-23', '30-Sep-23',
                '7-Oct-23', '7-Oct-23', '7-Oct-23', '7-Oct-23', '14-Oct-23', '14-Oct-23'],
    'Hari': ['Sabtu', 'Sabtu', 'Sabtu', 'Sabtu', 'Sabtu', 'Sabtu',
             'Sabtu', 'Sabtu', 'Sabtu', 'Sabtu', 'Sabtu', 'Sabtu'],
    'Jam Mulai': ['13:00', '15:45', '18:15', '19:15', '10:30', '13:30',
                  '09:00', '11:30', '14:00', '16:30', '09:00', '11:30'],
    'Jam Selesai': ['15:30', '18:15', '19:15', '20:15', '13:00', '16:00',
                    '11:00', '13:00', '16:00', '18:00', '11:00', '13:00'],
    'Kuliah': ['CS1002 - Computer and Network Security (CS23A)',
               'CS1002 - Computer and Network Security (CS23A)',
               'CS1002 - Computer and Network Security (CS23A)',
               'CS1002 - Computer and Network Security (CS23A)',
               'CS1206 - Mobile Computing (CS22B)',
               'CS1206 - Mobile Computing (CS22B)',
               'CS2001 - Artificial Intelligence (CS21C)',
               'CS2001 - Artificial Intelligence (CS21C)',
               'CS2002 - Machine Learning (CS21D)',
               'CS2002 - Machine Learning (CS21D)',
               'CS3001 - Data Science (CS20A)',
               'CS3001 - Data Science (CS20A)'],
    'Ruang': ['Online', 'Online', 'Online', 'Online', 'Online', 'Online',
              'Lab 1', 'Lab 1', 'Lab 2', 'Lab 2', 'Lab 3', 'Lab 3']
}

dosen_data = {
    'Nama': ['Dr. Andi', 'Dr. Budi', 'Dr. Citra', 'Dr. Dian', 'Dr. Eko'],
    'Mata Kuliah': ['CS1002', 'CS1206', 'CS2001', 'CS2002', 'CS3001']
}
mata_kuliah_data = {
    'Kode': ['CS1002', 'CS1206', 'CS2001', 'CS2002', 'CS3001'],
    'Nama': ['Computer and Network Security', 'Mobile Computing', 'Artificial Intelligence', 'Machine Learning', 'Data Science']
}

df_dosen = pd.DataFrame(dosen_data)
df_mata_kuliah = pd.DataFrame(mata_kuliah_data)
df = pd.DataFrame(data)

# Define the genetic algorithm components
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(df))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_schedule(individual):
    df['Scheduled'] = individual
    scheduled = df[df['Scheduled'] == 1]
    fitness = 0
    for i in range(len(scheduled)):
        start_time_i = pd.to_datetime(scheduled.iloc[i]['Jam Mulai'])
        end_time_i = pd.to_datetime(scheduled.iloc[i]['Jam Selesai'])
        for j in range(i + 1, len(scheduled)):
            start_time_j = pd.to_datetime(scheduled.iloc[j]['Jam Mulai'])
            end_time_j = pd.to_datetime(scheduled.iloc[j]['Jam Selesai'])
            if (start_time_i < end_time_j) and (start_time_j < end_time_i):
                fitness += 1
            if scheduled.iloc[i]['Ruang'] == scheduled.iloc[j]['Ruang']:
                fitness += 1
    return fitness,

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval_schedule)

def run_ga():
    random.seed(64)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", lambda x: sum(x) / len(x))
    stats.register("min", min)
    stats.register("max", max)
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.1, ngen=10, stats=stats, halloffame=hof, verbose=True)
    return hof[0]

app = Flask(__name__)

@app.route('/')
def index():
    best_individual = run_ga()
    df['Scheduled'] = best_individual
    schedule = df[df['Scheduled'] == 1].to_dict(orient='records')
    return render_template('index.html', schedule=schedule)

@app.route('/dosen')
def dosen():
    dosen_list = df_dosen.to_dict(orient='records')
    return render_template('dosen.html', dosen_list=dosen_list)

@app.route('/mata_kuliah')
def mata_kuliah():
    mata_kuliah_list = df_mata_kuliah.to_dict(orient='records')
    return render_template('mata_kuliah.html', mata_kuliah_list=mata_kuliah_list)

@app.route('/generate', methods=['POST'])
def generate():
    best_individual = run_ga()
    df['Scheduled'] = best_individual
    schedule = df[df['Scheduled'] == 1].to_dict(orient='records')
    return jsonify(schedule)

if __name__ == "__main__":
    app.run(debug=True)
