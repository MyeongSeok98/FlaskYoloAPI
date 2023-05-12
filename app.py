from flask import Flask, render_template, request
import tensorflow as tf
import cv2
import  numpy as np
import json

# 플라스크 시작
app = Flask(__name__)

model = tf.keras.models.load_model('model/model.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

path = './image/Zzim.jpg'
with open(path, 'rb') as f:
	data = f.read()

# 루트 파일
@app.route('/')
def index():
	return 'Hello Data Science Optimizers'

# HTML 파일 추가
@app.route('/home')
def home():
	return render_template('index.html')


@app.route('/predict', methods=['GET'])
def predict():
	# 이미지 읽어옴
	img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)

	# 이미지 416 416으로 리사이징 시킴
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = cv2.resize(img, (416, 416))
	img = img / 255.0
	img = np.expand_dims(img, axis=0)

	# 예측 수행
	predictions = model.predict(img)

	# 클래스, 확률, x, y, w, h 추출
	results = []
	for output in predictions:
		for detection in output:
			obj = {
				"class": int(detection[4]),
				"confidence": float(detection[5]),
				"x": int(detection[0]),
				"y": int(detection[1]),
				"w": int(detection[2] - detection[0]),
				"h": int(detection[3] - detection[1])
			}
			results.append(obj)

	# json으로 result 넘김
	return json.dumps(results)

if __name__ == '__main__':
	app.run(debug=True)