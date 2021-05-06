# nibble-sim

## About

A simulator to implement peer-to-peer communication strategies between 4^n nodes in a network.

### Authors

| Roll No. | Name |
| --- | --- |
| EDM18B037 | Mayank Navneet Mehta |
| EDM18B054 | Vishva Nilesh Bhate |

### Dependencies
- `networkx`
- `matplotlib`

To install the dependencies, run the following command
```bash
pip3 install -r requirements.txt
```

### Run
To execute the simulator on command line:
```bash
cd nibble-sim
python3 nibble_sim.py
```

To execute as a container:
1. Create the docker image using the `Dockerfile`:

```bash
docker build -t nibble-sim-docker .
```

2. Create a container using the docker image:

```bash
docker run -it --rm --name nib-sim-test nibble-sim-docker
```
The `nibble_sim.py` script is executed immediately.

3. Attach more shells to the container and execute:

```bash
python3 nibble_sim.py
```

> Note: You would need to connect your host system's X11 server with the container to visualize the network.

Click [here](./docs/Home.md) to view at our documentation and notes.
