import matplotlib.pyplot as plt


def plot_energy_produced(step_df):
    plt.rcParams["figure.figsize"] = (8, 5)
    plt.rcParams['font.size'] = 12

    # Plotting energy produced
    plt.plot(step_df['energy_generated_generator'], color='darkred', label='generator', alpha=0.7)
    plt.plot(step_df['discharged'], color='yellow', label='battery', alpha=0.5)
    plt.plot(step_df['energy_generated_solar'], color='orange', label='solar energy', alpha=1)
    plt.plot(step_df['energy_generated_wind'], color='darkblue', label='wind energy', alpha=1)

    # Adding labels and title
    plt.xlabel('Time')
    plt.ylabel('Energy (kWh)')
    plt.title('Energy mix')

    # Moving legend outside to the right and centering
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Show the plot
    plt.show()


def plot_demand_load(step_df, k=200):
    plt.rcParams["figure.figsize"] = (8, 5)
    plt.rcParams['font.size'] = 12

    # Plotting energy demand and load for step_df
    plt.plot(step_df['energy_load'][:k], color='darkred', label='Energy load')
    plt.plot(step_df['energy_demand'][:k], color='darkgreen', label='Energy demand')
    plt.xlabel('Time ($h$)')
    plt.ylabel('Energy ($kWh$)')
    plt.title('Energy Supply and Demand')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Show the plot
    plt.show()


def plot_solar_power(step_df, k=200):
    plt.rcParams["figure.figsize"] = (8, 5)
    plt.rcParams['font.size'] = 12

    # Plotting solar for step_df
    working_status = [d.get("solar") for d in step_df['actions_adjusting_status']]
    working_status = [v * 100 for v in working_status]
    plt.scatter(range(k), working_status[:k], color='green', label='working status', alpha=1, s=15)
    plt.plot(step_df['solar_irradiance'][:k], color='orange', label='solar irradiance', alpha=1)
    plt.plot(step_df['energy_generated_solar'][:k], color='darkred', label='generated solar energy', alpha=1)
    plt.xlabel('Time ($h$)')
    plt.ylabel('Energy ($kWh$) & Solar Irradiance ($W/m^2$)')
    plt.title('Solar Energy Overview')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Show the plot
    plt.show()
