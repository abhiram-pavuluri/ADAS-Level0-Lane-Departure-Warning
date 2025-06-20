****ADAS-Leve0-Lane-Departure-Warning | ADAS_Journey_0_1_Lane_Departure_Warning_V0.1*****

Self-taught a Level 0 ADAS Lane Departure Warning System implementation using Python and OpenCV. Part of a hands-on journey into autonomous driving technology by an ADAS engineer.


****ADAS Level 0 - Lane Departure Warning System****

This project is part of my self-driven journey into the world of Advanced Driver Assistance Systems (ADAS). With two years of industry experience as an ADAS tester, I often found myself distanced from the core algorithms. To bridge that gap, I’ve begun building ADAS features from the ground up using Python and OpenCV—starting here with a **Level 0 Lane Departure Warning (LDW)** system.


** What is Lane Departure Warning (LDW)?**
Lane Departure Warning is a basic yet critical ADAS feature that monitors lane markings and alerts the driver when the vehicle unintentionally drifts out of its lane.


**What This Project Does**

- Captures GTA 5 window 
- Uses basic image processing techniques, including:
  - Region of Interest (ROI) masking
  - Perspective transform (bird’s eye approximation)
  - Histogram-based lane base point detection
- Detects **lane starting positions** in a front-view driving perspective
- Triggers a visual lane departure warning when drift is detected

**Tech Stack**
- Python
- OpenCV
- NumPy
- MSS

**Features Implemented**
- ✅ Real-time video processing
- ✅ Lane detection with adjustable ROI & HSV
-  Left/right lane smoothing with historical memory (planning for v1.1)
- ✅ Visual warning overlay on drift detection


**What's Next?**
I will be progressing through ADAS levels and building each function incrementally:
1. Level 0 - LDW ✅
2. Level 1 - Lane Keep Assist (LKA)
3. Level 1 - Adaptive Cruise Control (ACC)
4. Level 2+ - Sensor fusion, path planning, etc.

Stay tuned!

Author
Abhiram Pavuluri  
ADAS Engineer | Self-taught Developer | Building Vision One Frame at a Time  
India  
🔗 [LinkedIn](https://www.linkedin.com/in/abhiram-pavuluri/)


This is a learning-first project. Suggestions and improvements are welcome!
_If you find this helpful or inspiring, give it a star and follow my journey on LinkedIn!_


**Versioning**

This project follows semantic versioning:

- **v1.0**: Initial release – basic LDW implementation with OpenCV & HSV

**Improvements for Later Version**
- Completion of leftover Sliding Window Development in V1.0
- Experimentation with Canny Edge Detections & Hough Line Transforms as alternative strategies
- Full lane tracking with polynomial fits and curvature estimation
