# nibble-sim

## About

A simulator to implement peer-to-peer communication strategies between 4^n nodes in a network.

### Authors

| Roll No. | Name |
| --- | --- |
| EDM18B037 | Mayank Navneet Mehta |
| EDM18B054 | Vishva Nilesh Bhate |

### Test using docker

1. Create the docker image using the `Dockerfile`:

```bash
docker build -t nibble-sim-docker .
```

2. Create a container using the docker image:

```bash
docker run -it --rm --name nib-sim-test nibble-sim-docker
```

3. Attach a shell to the container and execute:

```bash
python3 nibble_sim.py
```

Click [here](./docs/Home.md) to view at our documentation and notes.
