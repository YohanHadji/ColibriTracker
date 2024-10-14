


# Measure the prediction time
import time
start = time.time()
prediction = model.predict("rocket.jpg", confidence=40, overlap=30)
## get predictions on hosted images
# prediction = model.predict("rocket.jpg", hosted=True)
print(prediction.json())
print("Prediction time: ", time.time()-start)