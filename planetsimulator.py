import plotly.graph_objs as go
import numpy as np


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class CelestialBody:
    def __init__(self, mass, position):
        self.mass = mass
        self.position = position


class Planet(CelestialBody):
    def __init__(self, name, mass, distance_from_sun):
        super().__init__(mass, Vector3D(0, distance_from_sun, 0))
        self.name = name

    def calculate_orbit(self, num_points=100):
        theta = np.linspace(0, 2 * np.pi, num_points)
        orbit_x = np.cos(theta) * self.position.y
        orbit_y = np.sin(theta) * self.position.y
        orbit_z = np.zeros(num_points)
        return orbit_x, orbit_y, orbit_z


class Sun(CelestialBody):
    def __init__(self, mass):
        super().__init__(mass, Vector3D(0, 0, 0))


# Funktion til at simulere og visualisere solsystemet
def simulate_and_visualize(sun, planets, num_iterations, delta_t):
    # Opret figurobjekt
    fig = go.Figure()

    # Tilføj Solen til figuren
    fig.add_trace(go.Scatter3d(
        x=[sun.position.x],
        y=[sun.position.y],
        z=[sun.position.z],
        mode='markers',
        marker=dict(
            size=10,
            color='yellow'
        ),
        name='Sun'
    ))

    # Tilføj planeter til figuren som punkter
    for planet in planets:
        # Beregn planetens bane
        orbit_x, orbit_y, orbit_z = planet.calculate_orbit(num_points=100)

        # Tilføj planetens bane til figuren
        fig.add_trace(go.Scatter3d(
            x=orbit_x,
            y=orbit_y,
            z=orbit_z,
            mode='lines',
            line=dict(
                color='blue',
                width=1
            ),
            name=f'{planet.name} Orbit'
        ))

        # Tilføj planeten som et punkt
        fig.add_trace(go.Scatter3d(
            x=[planet.position.x],
            y=[planet.position.y],
            z=[planet.position.z],
            mode='markers',
            marker=dict(
                size=5,
                color='red',
            ),
            name=planet.name
        ))

    # Indstil layout for figuren
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z'),
        )
    )

    # Vis figuren
    fig.show()


# Main-funktionen
def main():
    # Opret instanser af planeter og Solen
    sun = Sun(mass=1.989e30)  # Solens masse i kg
    mercury = Planet(name="Mercury", mass=3.285e23, distance_from_sun=57.9e9)  # Merkur
    venus = Planet(name="Venus", mass=4.867e24, distance_from_sun=108.2e9)  # Venus
    earth = Planet(name="Earth", mass=5.972e24, distance_from_sun=149.6e9)  # Jorden
    mars = Planet(name="Mars", mass=6.39e23, distance_from_sun=227.9e9)  # Mars
    jupiter = Planet(name="Jupiter", mass=1.898e27, distance_from_sun=778.5e9)  # Jupiter
    saturn = Planet(name="Saturn", mass=5.683e26, distance_from_sun=1.434e12)  # Saturn
    uranus = Planet(name="Uranus", mass=8.681e25, distance_from_sun=2.871e12)  # Uranus
    neptune = Planet(name="Neptune", mass=1.024e26, distance_from_sun=4.495e12)  # Neptun

    # Simulér og visualisér solsystemet
    num_iterations = 365
    delta_t = 86400
    simulate_and_visualize(sun, [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune], num_iterations, delta_t)


if __name__ == "__main__":
    main()
