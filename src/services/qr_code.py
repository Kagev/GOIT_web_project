import qrcode


def generate_qr_code(data: object) -> object:
	"""
	Generate qr code
	:rtype: object
	:return:
	:param data:
	:return:
	"""
	# Create QR-code
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(data)
	qr.make(fit=True)

	# generation image for QR-code
	qr_image = qr.make_image(fill_color="black", back_color="white")

	return qr_image
