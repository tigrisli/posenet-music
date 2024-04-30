import cv2
from PoseNet.pose import detect_pose

def main():
    detect_pose(display_in_cv_image, quit_on_key=True)

def display_in_cv_image(image, keypoints):
    cv2.imshow('Pose detector', image)
    if keypoints:
        print_keypoints(keypoints)

def print_keypoints(keypoints):
    # Assuming keypoints is a list of (x, y, confidence) for each keypoint
    for idx, keypoint in enumerate(keypoints):
        print(f"Keypoint {idx}: x={keypoint[0]}, y={keypoint[1]}, confidence={keypoint[2]}")

if __name__ == '__main__':
    main()
