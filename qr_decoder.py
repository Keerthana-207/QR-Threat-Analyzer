import cv2


def decode_qr(image_path):

    detector = cv2.QRCodeDetector()

    image = cv2.imread(image_path)

    if image is None:
        return {
            "success": False,
            "message": "Invalid image"
        }


    data, points, _ = detector.detectAndDecode(image)


    if data:

        return {
            "success": True,
            "data": [data]
        }


    return {
        "success": False,
        "message": "No QR detected"
    }