import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model

# Loading VGG16 model pre-trained on ImageNet, excluding top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Adding custom top layers for your binary classification
x = base_model.output
x = Flatten()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compiling the model with binary cross-entropy loss
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Loading and preprocessing your dataset
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)  # Including validation split
train_generator = train_datagen.flow_from_directory(
    'Train_Folder_Directory', # content/drive/directory/train (pictures should be inside a folder named 'images' {...directory/valid/images})
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training')

validation_generator = train_datagen.flow_from_directory(
    'Valid_Folder_Directory', # content/drive/directory/valid (pictures should be inside a folder named 'images' {...directory/valid/images})
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation')

# Training the model
model.fit(train_generator, validation_data=validation_generator, epochs=10)

# Saving the model
model.save('weed_detection_model.h5')

"""
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SAMPLE OUTPUT

Found 225 images belonging to 2 classes.
Found 55 images belonging to 2 classes.
Epoch 1/10
8/8 [==============================] - 40s 2s/step - loss: 6.4857 - accuracy: 0.6578 - val_loss: 1.4303 - val_accuracy: 0.9091
Epoch 2/10
8/8 [==============================] - 4s 423ms/step - loss: 0.5929 - accuracy: 0.9067 - val_loss: 0.3930 - val_accuracy: 0.9091
Epoch 3/10
8/8 [==============================] - 4s 434ms/step - loss: 0.3734 - accuracy: 0.9067 - val_loss: 0.5685 - val_accuracy: 0.9091
Epoch 4/10
8/8 [==============================] - 4s 483ms/step - loss: 0.4553 - accuracy: 0.9067 - val_loss: 0.3093 - val_accuracy: 0.9091
Epoch 5/10
8/8 [==============================] - 4s 418ms/step - loss: 0.3222 - accuracy: 0.9067 - val_loss: 0.3244 - val_accuracy: 0.9091
Epoch 6/10
8/8 [==============================] - 4s 423ms/step - loss: 0.3348 - accuracy: 0.9067 - val_loss: 0.3046 - val_accuracy: 0.9091
Epoch 7/10
8/8 [==============================] - 4s 445ms/step - loss: 0.3465 - accuracy: 0.9067 - val_loss: 3.5405 - val_accuracy: 0.0909
Epoch 8/10
8/8 [==============================] - 4s 554ms/step - loss: 0.4477 - accuracy: 0.9022 - val_loss: 0.3375 - val_accuracy: 0.9091
Epoch 9/10
8/8 [==============================] - 4s 424ms/step - loss: 0.4629 - accuracy: 0.9067 - val_loss: 0.3606 - val_accuracy: 0.9091
Epoch 10/10
8/8 [==============================] - 4s 441ms/step - loss: 0.3659 - accuracy: 0.9067 - val_loss: 0.3675 - val_accuracy: 0.9091
/usr/local/lib/python3.10/dist-packages/keras/src/engine/training.py:3103: UserWarning: You are saving your model as an HDF5 file via `model.save()`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')`.
  saving_api.save_model(
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""

# Loading the saved keras model { model.save('weed_detection_model.h5' }

model = tf.keras.models.load_model('weed_detection_model.h5'

# Converting the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)