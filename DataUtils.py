import numpy as np

# encoder (x, y) + altitude (z) + imu
# x y z theta
# x & y are encoder counts
# z altitude
# theta

class DataInterface:
    def __init__(self, gps, imu, encoders):
        self.gps_data = np.loadtxt(gps, delimiter=",")
        self.imu_data = np.loadtxt(imu, delimiter=",")
        self.encoders_data = np.loadtxt(encoders, delimiter=",")
        self._current_gps_time = 0
        self._current_imu_time = -1
        self._current_encoders_time = -1

    def read(self):
        if self._current_gps_time >= self.get_end_time():
            raise Exception("We have reached the end of the data...")

        gps_curr_time = self.gps_data[self._current_gps_time, 0]
        imu_time_idx = np.where((self.imu_data[self._current_imu_time + 1:, 0] - gps_curr_time) > 1e-5)[0]
        encoders_time_idx = np.where((self.encoders_data[self._current_encoders_time + 1:, 0] - gps_curr_time) > 1e-5)[0]

        if len(imu_time_idx) == 0 or len(encoders_time_idx) == 0:
            raise Exception("We have reached the end of the data...")
        self._current_imu_time = imu_time_idx[0]
        self._current_encoders_time = encoders_time_idx[0]

        read_data = {
            "gps_data": self.gps_data[self._current_gps_time],
            "imu_data": self.imu_data[imu_time_idx][0],
            "encoders_data": self.encoders_data[encoders_time_idx][0]
        }

        self._current_gps_time += 1
        return read_data

    def get_current_time(self):
        return self._current_gps_time

    def get_end_time(self):
        return self.gps_data.shape[0]

if __name__ == "__main__":
    # Test with Pose Data
    data_interface = DataInterface(
        "/home/jay/Documents/urban16/sensor_data/gps.csv",
        "/home/jay/Documents/urban16/sensor_data/xsens_imu.csv",
        "/home/jay/Documents/urban16/sensor_data/encoder.csv"
    )

    try:
        while data_interface.get_current_time() < data_interface.get_end_time():
            time_data = data_interface.read()
            print(data_interface.get_current_time(), data_interface.get_end_time())
        print("Made it to the end!")
        data_interface.read()
    except Exception as e:
        print(data_interface.get_current_time())
        print(f"Exception caught, message: {e}")
