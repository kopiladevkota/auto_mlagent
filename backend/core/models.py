from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('data_scientist', 'Data Scientist'),
        ('business_user', 'Business User'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    company = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Project(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    STATUS_CHOICES = (
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='datasets')
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField(null=True, blank=True)
    rows = models.IntegerField(null=True, blank=True)
    columns = models.IntegerField(null=True, blank=True)
    column_names = models.JSONField(default=list)
    data_types = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class MLModel(models.Model):
    MODEL_TYPES = (
        ('classification', 'Classification'),
        ('regression', 'Regression'),
        ('clustering', 'Clustering'),
    )
    ALGORITHM_CHOICES = (
        ('xgboost', 'XGBoost'),
        ('random_forest', 'Random Forest'),
        ('neural_network', 'Neural Network'),
        ('svm', 'SVM'),
        ('lightgbm', 'LightGBM'),
        ('linear_regression', 'Linear Regression'),
        ('logistic_regression', 'Logistic Regression'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('training', 'Training'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('deployed', 'Deployed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='models')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    algorithm = models.CharField(max_length=50, choices=ALGORITHM_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    auc_roc = models.FloatField(null=True, blank=True)
    parameters = models.JSONField(default=dict)
    metrics = models.JSONField(default=dict)
    model_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trained_at = models.DateTimeField(null=True, blank=True)
    is_best = models.BooleanField(default=False)
    is_deployed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.algorithm})"


class TrainingJob(models.Model):
    STATUS_CHOICES = (
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='training_jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    logs = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"Job for {self.model.name} - {self.status}"


class ChatHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='chats', null=True, blank=True)
    query = models.TextField()
    response = models.TextField()
    context = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat: {self.query[:50]}..."


class Export(models.Model):
    FORMAT_CHOICES = (
        ('pickle', 'Pickle'),
        ('onnx', 'ONNX'),
        ('python_code', 'Python Code'),
        ('notebook', 'Jupyter Notebook'),
        ('fastapi_code', 'FastAPI Code'),
        ('dockerfile', 'Dockerfile'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='exports')
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='exports')
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    file_path = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Export {self.format} - {self.model.name}"