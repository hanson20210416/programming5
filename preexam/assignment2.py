from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size > 1:
    if rank == 0:
        comm.send('Hello from rank 0', dest=1)
    elif rank == 1:
        message = comm.recv(source=0)
        print(f"Rank {rank} received message: {message}")
else:
    print("Only one process available, no communication.")


