{
  "metadata": {
    "kernelspec": {
      "language": "python",
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.10.14",
      "mimetype": "text/x-python",
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "pygments_lexer": "ipython3",
      "nbconvert_exporter": "python",
      "file_extension": ".py"
    },
    "kaggle": {
      "accelerator": "gpu",
      "dataSources": [
        {
          "sourceId": 9218913,
          "sourceType": "datasetVersion",
          "datasetId": 5574989
        },
        {
          "sourceId": 104646,
          "sourceType": "modelInstanceVersion",
          "isSourceIdPinned": True,
          "modelInstanceId": 87690,
          "modelId": 111923
        }
      ],
      "dockerImageVersionId": 30761,
      "isInternetEnabled": False,
      "language": "python",
      "sourceType": "script",
      "isGpuEnabled": True
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-30T19:42:56.034800Z\",\"iopub.execute_input\":\"2024-08-30T19:42:56.035652Z\",\"iopub.status.idle\":\"2024-08-30T19:43:08.146805Z\",\"shell.execute_reply.started\":\"2024-08-30T19:42:56.035610Z\",\"shell.execute_reply\":\"2024-08-30T19:43:08.145930Z\"}}\nimport tensorflow as tf\nfrom tensorflow.keras import layers, models\nfrom tensorflow.keras.preprocessing.image import ImageDataGenerator\nimport os\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-30T19:43:38.358297Z\",\"iopub.execute_input\":\"2024-08-30T19:43:38.359484Z\",\"iopub.status.idle\":\"2024-08-30T19:43:38.527269Z\",\"shell.execute_reply.started\":\"2024-08-30T19:43:38.359433Z\",\"shell.execute_reply\":\"2024-08-30T19:43:38.526454Z\"}}\ntrain_dir = '/kaggle/input/teethsetzeina/Teeth_Dataset/Training'\nval_dir = '/kaggle/input/teethsetzeina/Teeth_Dataset/Validation'\n\n# Data augmentation and normalization for training\ntrain_datagen = ImageDataGenerator(\n    rescale=1./255,\n    shear_range=0.2,\n    zoom_range=0.2,\n    horizontal_flip=True\n)\n\n# Only rescaling for validation\nval_datagen = ImageDataGenerator(rescale=1./255)\n\n# Load images in batches\ntrain_generator = train_datagen.flow_from_directory(\n    train_dir,\n    target_size=(224, 224),\n    batch_size=32,\n    class_mode='categorical'\n)\n\nval_generator = val_datagen.flow_from_directory(\n    val_dir,\n    target_size=(224, 224),\n    batch_size=32,\n    class_mode='categorical'\n)\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-30T19:45:55.317294Z\",\"iopub.execute_input\":\"2024-08-30T19:45:55.317683Z\",\"iopub.status.idle\":\"2024-08-30T19:45:56.011326Z\",\"shell.execute_reply.started\":\"2024-08-30T19:45:55.317646Z\",\"shell.execute_reply\":\"2024-08-30T19:45:56.010521Z\"}}\n# Load the base model with ResNet50 architecture, excluding the top (final) layers\nbase_model = tf.keras.applications.ResNet50(\n    weights=None,  # Do not load ImageNet weights\n    include_top=False,  # Do not include the fully-connected layer at the top\n    input_shape=(224, 224, 3)\n)\n\n# Load your own pre-trained weights\n#base_model.load_weights('/kaggle/input/your-dataset-folder-name/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5')\n\n# Add new top layers\nx = base_model.output\nx = layers.GlobalAveragePooling2D()(x)\nx = layers.Dense(1024, activation='relu')(x)\npredictions = layers.Dense(train_generator.num_classes, activation='softmax')(x)\n\n# Create the full model\nmodel = models.Model(inputs=base_model.input, outputs=predictions)\n\n# Freeze the base model layers during initial training\nfor layer in base_model.layers:\n    layer.trainable = False\n\n# Compile the model\nmodel.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-30T19:46:26.429356Z\",\"iopub.execute_input\":\"2024-08-30T19:46:26.430146Z\",\"iopub.status.idle\":\"2024-08-30T19:50:34.211000Z\",\"shell.execute_reply.started\":\"2024-08-30T19:46:26.430105Z\",\"shell.execute_reply\":\"2024-08-30T19:50:34.210226Z\"}}\n# Train the model\nhistory = model.fit(\n    train_generator,\n    steps_per_epoch=train_generator.samples // train_generator.batch_size,\n    validation_data=val_generator,\n    validation_steps=val_generator.samples // val_generator.batch_size,\n    epochs=10\n)\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-30T19:56:31.597131Z\",\"iopub.execute_input\":\"2024-08-30T19:56:31.597553Z\",\"iopub.status.idle\":\"2024-08-30T19:56:32.148102Z\",\"shell.execute_reply.started\":\"2024-08-30T19:56:31.597515Z\",\"shell.execute_reply\":\"2024-08-30T19:56:32.147124Z\"}}\nmodel.save('/kaggle/working/finetuned_model.h5')\nprint(\"Model saved successfully as a .h5 file!\")\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-30T20:00:12.363254Z\",\"iopub.execute_input\":\"2024-08-30T20:00:12.364247Z\",\"iopub.status.idle\":\"2024-08-30T20:00:12.443323Z\",\"shell.execute_reply.started\":\"2024-08-30T20:00:12.364205Z\",\"shell.execute_reply\":\"2024-08-30T20:00:12.442124Z\"}}\n# Streamlit app code here, for example:\nimport streamlit as st\nimport tensorflow as tf\nfrom tensorflow.keras.preprocessing import image\nimport numpy as np\nfrom PIL import Image\n\n# Load the trained model\nmodel = tf.keras.models.load_model('/kaggle/working/finetuned_model.h5')\n\n# Function to load and preprocess the image\ndef load_and_preprocess_image(uploaded_file):\n    img = Image.open(uploaded_file)\n    img = img.resize((224, 224))\n    img_array = image.img_to_array(img)\n    img_array = np.expand_dims(img_array, axis=0)\n    img_array = img_array / 255.0  # Normalize to [0, 1]\n    return img_array\n\n# Streamlit app interface\nst.title(\"Image Classification with ResNet-50\")\nst.write(\"Upload an image to classify it.\")\n\nuploaded_file = st.file_uploader(\"Choose an image...\", type=\"jpg\")\n\nif uploaded_file is not None:\n    # Display the uploaded image\n    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)\n    \n    # Preprocess the image\n    img_array = load_and_preprocess_image(uploaded_file)\n    \n    # Make a prediction\n    prediction = model.predict(img_array)\n    predicted_class = np.argmax(prediction, axis=1)\n    \n    # Display the prediction\n    st.write(f\"Predicted class: {predicted_class[0]}\")\n\n# Now run the app\n!streamlit run app.py\n\n\n# %% [code]\n# Streamlit app code here:\nimport streamlit as st\nimport tensorflow as tf\nfrom tensorflow.keras.preprocessing import image\nimport numpy as np\nfrom PIL import Image\n\n# Load the trained model\nmodel = tf.keras.models.load_model('/kaggle/working/finetuned_model.h5')\n\n# Function to load and preprocess the image\ndef load_and_preprocess_image(uploaded_file):\n    img = Image.open(uploaded_file)\n    img = img.resize((224, 224))\n    img_array = image.img_to_array(img)\n    img_array = np.expand_dims(img_array, axis=0)\n    img_array = img_array / 255.0  # Normalize to [0, 1]\n    return img_array\n\n# Streamlit app interface\nst.title(\"Image Classification with ResNet-50\")\nst.write(\"Upload an image to classify it.\")\n\nuploaded_file = st.file_uploader(\"Choose an image...\", type=\"jpg\")\n\nif uploaded_file is not None:\n    # Display the uploaded image\n    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)\n    \n    # Preprocess the image\n    img_array = load_and_preprocess_image(uploaded_file)\n    \n    # Make a prediction\n    prediction = model.predict(img_array)\n    predicted_class = np.argmax(prediction, axis=1)\n    \n    # Display the prediction\n    st.write(f\"Predicted class: {predicted_class[0]}\")\n\n",
      "metadata": {
        "_uuid": "78085cf0-6293-4a6d-b068-5e1f6e2f9bab",
        "_cell_guid": "847c7a55-02d6-4cac-a6dd-fc6b4af45250",
        "collapsed": False,
        "jupyter": {
          "outputs_hidden": False
        },
        "trusted": True
      },
      "execution_count": None,
      "outputs": []
    }
  ]
}
