import numpy as np

# encoder (x, y) + altitude (z) + imu
# x y z theta
# x & y are encoder counts
# z altitude
# theta

class DataInterface:
    def __init__(self, file_path):
        self.data = np.loadtxt(file_path, delimiter=",")
        self._current_time = 0

    def read(self):
        if self._current_time >= self.get_end_time():
            raise Exception("We have reached the end of the data...")
        read_data = self.data[self._current_time, :]
        self._current_time += 1
        return read_data

    def get_current_time(self):
        return self._current_time

    def get_end_time(self):
        return self.data.shape[0]

if __name__ == "__main__":
    # Test with Pose Data
    pose = DataInterface("/home/jay/Documents/global_pose.csv")

    while pose.get_current_time() < pose.get_end_time():
        time_data = pose.read()
        print(time_data)

    try:
        pose.read()
    except Exception as e:
        print(f"Exception caught, message: {e}")
