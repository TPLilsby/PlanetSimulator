import plotly.graph_objs as go
import numpy as np

# Definition af klasser og funktioner

class Planet:
    def __init__(self, name, mass, distance_from_sun):
        self.name = name
        self.mass = mass
        self.distance_from_sun = distance_from_sun
        self.position = 0  # Start position
        self.velocity = 0  # Start velocity

    def update_position_and_velocity(self, force, delta_t):
        acceleration = force / self.mass
        self.velocity += acceleration * delta_t
        self.position += self.velocity * delta_t


class Sun:
    def __init__(self, mass):
        self.mass = mass


def calculate_gravitational_force(planet, sun):
    gravitational_constant = 6.67430e-11
    distance = planet.distance_from_sun
    force = gravitational_constant * (sun.mass * planet.mass) / distance ** 2
    return force


def get_color_scale(num_planets):
    colors = []
    for i in range(num_planets):
        colors.append("hsl(" + str(int(360 * i / num_planets)) + ",50%,50%)")
    return colors


def simulate_and_visualize(sun, planets, num_iterations, delta_t):
    # Initialize lists to store planet positions for each iteration
    planet_positions = [[] for _ in range(len(planets))]

    # Simulation loop
    for i in range(num_iterations):
        for j, planet in enumerate(planets):
            # Calculate the gravitational force from the Sun on each planet
            force = calculate_gravitational_force(planet, sun)

            # Update the planet's position and velocity
            planet.update_position_and_velocity(force, delta_t)

            # Store the planet's position for this iteration
            planet_positions[j].append(planet.position)

    # Create frames for the animation
    frames = []
    for i in range(num_iterations):
        frame_data = []
        for j, planet in enumerate(planets):
            frame_data.append(go.Scatter(x=[planet_positions[j][i]], y=[0], mode='markers', name=planet.name,
                                         marker=dict(color=get_color_scale(len(planets))[j]),
                                         hovertext=planet.name))
        frames.append({'data': frame_data, 'name': f'Frame {i}', 'layout': go.Layout(
            title='Solar System Simulation Animation',
            xaxis=dict(title='Distance from Sun (m)'),
            yaxis=dict(title='Y-axis'),
            template='plotly_dark'
        )})

    # Create the animation
    animation = go.Figure(frames=frames)

    # Add circles representing planet orbits
    for j, planet in enumerate(planets):
        orbit_x = []
        orbit_y = []
        for theta in np.linspace(0, 2 * np.pi, 100):
            orbit_x.append(planet.distance_from_sun * np.cos(theta))
            orbit_y.append(planet.distance_from_sun * np.sin(theta))
        animation.add_trace(go.Scatter(x=orbit_x, y=orbit_y, mode='lines',
                                       name=planet.name,
                                       line=dict(color=get_color_scale(len(planets))[j]),
                                       showlegend=False,
                                       hovertext=planet.name))

    # Add 3D models of planets at some position on their orbits
    for j, planet in enumerate(planets):
        model_trace = go.Scatter3d(
            x=[orbit_x[j]],
            y=[orbit_y[j]],
            z=[0],  # Just for visualization, the Z-coordinate can be adjusted as needed
            mode='markers',  # Use mode 'markers' for 3D models
            marker=dict(
                size=10,  # Adjust size as needed
                color=get_color_scale(len(planets))[j],  # Adjust color as needed
                opacity=1,
                symbol=f"https://raw.githubusercontent.com/plotly/models/master/planets/{planet.name.lower()}.glb",  # 3D model URL
            ),
            name=planet.name + " Model"
        )
        animation.add_trace(model_trace)

    # Show animation
    animation.show()


def main():
    # Create instances of planets and the Sun
    sun = Sun(mass=1.989e30)  # Suns mass in kg
    mercury = Planet(name="Mercury", mass=3.285e23, distance_from_sun=57.9e9)  # Mercury
    venus = Planet(name="Venus", mass=4.867e24, distance_from_sun=108.2e9)  # Venus
    earth = Planet(name="Earth", mass=5.972e24, distance_from_sun=149.6e9)  # Earth
    mars = Planet(name="Mars", mass=6.39e23, distance_from_sun=227.9e9)  # Mars
    jupiter = Planet(name="Jupiter", mass=1.898e27, distance_from_sun=778.5e9)  # Jupiter
    saturn = Planet(name="Saturn", mass=5.683e26, distance_from_sun=1.434e12)  # Saturn
    uranus = Planet(name="Uranus", mass=8.681e25, distance_from_sun=2.871e12)  # Uranus
    neptune = Planet(name="Neptune", mass=1.024e26, distance_from_sun=4.495e12)  # Neptune

    # Simulate and visualize the solar system
    num_iterations = 365
    delta_t = 86400
    simulate_and_visualize(sun, [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune], num_iterations, delta_t)


if __name__ == "__main__":
    main()
