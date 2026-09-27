# Reading in the order you will use it

Do each exercise before moving on; reading alone will not prepare you to explain model decisions.

1. Python environments and VS Code
https://code.visualstudio.com/docs/python/environments
Exercise: create .venv, select its interpreter, and run the synthetic demo. Explain why dependencies are isolated.

2. Tensors, datasets, gradients and training loops
https://docs.pytorch.org/tutorials/beginner/basics/intro.html
Exercise: finish the basic tutorial; explain batch size, epoch, loss, gradient and learning rate without looking at notes.

3. Transfer learning
https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial
Exercise: compare a frozen encoder with fine tuning. Explain which weights change and why pretrained image features may help.

4. Building change detection and segmentation
https://levir.buaa.edu.cn/publications/remotesensing-798405-eng.pdf
https://github.com/justchenhao/LEVIR
Exercise: draw the two-image input and pixel-mask output; identify illumination, shadows and registration as sources of false change. Read the dataset section first; the attention architecture is optional advanced reading.

5. Evaluation and leakage
https://scikit-learn.org/stable/modules/model_evaluation.html
https://scikit-learn.org/stable/common_pitfalls.html
Exercise: calculate precision, recall, F1 and IoU from TP/FP/FN. Explain why mostly unchanged images can yield high accuracy with a useless model. Explain why adjacent crops must not cross partitions.

6. Anomaly and novelty detection
https://scikit-learn.org/stable/modules/outlier_detection.html
Exercise: explain why an unusual tile is not necessarily a building change. Compare an Isolation Forest ranking with supervised predictions on reviewed data.

7. Satellite data and alignment (later UAE stage)
https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel2.html
https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S2L2A.html
https://rasterio.readthedocs.io/en/stable/topics/reproject.html
Exercise: explain spatial resolution, spectral bands, reflectance, CRS, reprojection and cloud masking. Check that two pixels represent the same ground location.

8. Deployment and ONNX
https://docs.pytorch.org/tutorials/beginner/onnx/export_simple_model_to_onnx_tutorial.html
https://onnxruntime.ai/docs/get-started/with-python.html
Exercise: export your trained model, compare outputs and mask metrics with PyTorch, and time repeated CPU inference. Explain that ONNX is an interchange format, not a training algorithm.

9. Company context
https://space42.ai/en/foresight-viewpoint/articles/2025/giq---from-manual-analysis-to-ai-driven-insight/
Exercise: connect your prototype to analyst review and explain the changes needed for multiple sensors and production use. Do not assume this specific vacancy belongs to the GIQ team.

Links selected 26 September 2026. Tutorial versions can change: record package versions with your experiment results.
