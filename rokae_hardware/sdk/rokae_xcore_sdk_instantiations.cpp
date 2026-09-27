#include <array>
#include <string>
#include <vector>

#include "rokae/robot.h"

namespace rokae {

// libxCoreSDK.a exports getStateData for std::array<double, N> but not std::vector<double>.
// rokae_hardware uses std::vector for joint buffers; provide adapter inside isolated SDK DSO.
template <>
int BaseRobot::getStateData<std::vector<double>>(const std::string &fieldName,
                                                 std::vector<double> &data)
{
  switch (data.size()) {
    case 5: {
      std::array<double, 5> arr{};
      const int ret = getStateData(fieldName, arr);
      if (ret == 0) {
        data.assign(arr.begin(), arr.end());
      }
      return ret;
    }
    case 6: {
      std::array<double, 6> arr{};
      const int ret = getStateData(fieldName, arr);
      if (ret == 0) {
        data.assign(arr.begin(), arr.end());
      }
      return ret;
    }
    case 7: {
      std::array<double, 7> arr{};
      const int ret = getStateData(fieldName, arr);
      if (ret == 0) {
        data.assign(arr.begin(), arr.end());
      }
      return ret;
    }
    default:
      return -1;
  }
}

}  // namespace rokae
