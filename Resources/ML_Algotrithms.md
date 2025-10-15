# Machine Learning Overview

## 1. What is Machine Learning?

Machine Learning (ML) is a subset of Artificial Intelligence (AI) focused on building systems that can learn from data, detect patterns, and make decisions with minimal human intervention.

In more formal terms, in ML you have data (inputs/features) and outcomes (labels or structural properties). You use algorithms to build a model that maps inputs to outputs, or to infer structure in the data.

The video emphasizes that there are two major paradigms introduced early: supervised learning and unsupervised learning (and implicitly, a nod toward more advanced ones, though not in depth).

### Supervised vs Unsupervised Learning

- **Supervised learning:** The model is trained on labeled data — that is, each training example has an input *x* and an output *y*. The algorithm’s goal is to learn the mapping from *x → y*.
  - **Tasks:** regression (predicting continuous values) or classification (predicting discrete categories / classes).

- **Unsupervised learning:** The model is given only inputs (unlabeled), and must infer underlying structure, groupings, or representations.
  - **Tasks:** clustering (group similar items), dimensionality reduction, parameter estimation, density estimation, anomaly detection, etc.

The video first walks through supervised algorithms, then returns to unsupervised ones.

---

## 2. Supervised Learning Algorithms

Below is a more detailed view of the supervised learning methods covered in the video and some additional insight.

### 2.1 Linear Regression

**What:** One of the simplest regression models. You assume a linear relationship between input features \(x\) and continuous target \(y\).

\[ y = w^T x + b + \epsilon \]

where \(w\) and \(b\) are parameters to learn, and \(\epsilon\) is noise.

**How it learns:** Typically via minimizing a loss (e.g. Mean Squared Error) using techniques like ordinary least squares or gradient descent.

**Use cases:** Predicting numerical quantities (e.g. house prices, temperatures, sales numbers).

**Caveats / Assumptions:**
- Assumes linear relationship.
- Sensitive to outliers.
- Multicollinearity among features can degrade performance.
- Extrapolation outside the training data may be unreliable.

### 2.2 Logistic Regression

**What:** A classification method (for binary classification). The model estimates probability of class membership:

\[ P(y=1 | x) = \sigma(w^T x + b) \]

where \(\sigma\) is the sigmoid (logistic) function.

**How it learns:** By maximizing the log-likelihood (or equivalently minimizing cross-entropy loss) using gradient-based methods.

**Use cases:** Binary classification tasks (spam vs not spam, disease vs healthy, etc.).

**Remarks:**
- Although its name has “regression,” it’s actually for classification.
- You can extend it to multiclass problems (e.g. softmax / multinomial logistic regression).

### 2.3 K-Nearest Neighbors (KNN)

**What:** Instance-based (a “lazy learner”) classifier/regressor. To classify a new point, it looks at the *k* nearest neighbors in the training set and takes a majority vote (or average, for regression).

**How it works:**
1. Store all training instances.
2. Given a new point, compute its distance (e.g. Euclidean) to all training points.
3. Pick the *k* closest ones, and decide the label based on them.

**Advantages:**
- Simple to understand and implement.
- No training phase (beyond storing data).

**Disadvantages / Caveats:**
- Computation can be expensive at prediction time (scales with dataset size).
- Sensitive to irrelevant / noisy features.
- Choice of *k* and the distance metric are critical.
- Curse of dimensionality: as dimensionality grows, distances become less meaningful.

### 2.4 Support Vector Machine (SVM)

**What:** A discriminative classifier that finds a hyperplane to separate classes with maximal margin.

**Key idea:** Among all possible separating hyperplanes, pick the one that maximizes the margin (distance) between the nearest points (support vectors) of each class.

**Kernel trick:** SVMs allow mapping input data into higher-dimensional feature spaces via kernels (e.g. polynomial, RBF), enabling non-linear separation.

**Advantages:**
- Effective in high-dimensional spaces.
- Works well when you have clear margins of separation.

**Caveats:**
- Choosing the correct kernel and hyperparameters (C, gamma, etc.) is essential.
- Can be less effective on noisy data or large datasets (training scales poorly with number of samples).

### 2.5 Naive Bayes

**What:** A probabilistic classification method based on Bayes’ theorem, with the “naive” assumption that feature values are conditionally independent given the class.

\[ P(y | x) \propto P(y) \prod_i P(x_i | y) \]

**Advantages:**
- Very fast to train and predict.
- Works well even with relatively small amounts of data.
- Especially good for text classification / spam detection / document classification.

**Caveats:**
- The independence assumption is often violated in real data, which can reduce performance.
- Some features might not be conditionally independent, leading to misestimation.

### 2.6 Decision Trees

**What:** A tree structure where internal nodes represent tests on features, branches are outcomes, and leaves represent class labels (or continuous values, in regression trees).

**How built:**
1. Use a top-down, greedy approach.
2. At each node, select the feature and threshold that best splits the data (maximizes some metric like information gain or Gini impurity).
3. Recursively split until stopping criteria (e.g. minimum samples, maximum depth, pure leaves).

**Advantages:**
- Intuitive, interpretable, visualizable.
- Handles both numerical and categorical features.
- Minimal data preparation: no scaling, no normalization required.

**Disadvantages / Caveats:**
- Prone to overfitting if tree is too deep / unconstrained.
- Unstable: small changes in data can lead to very different trees.
- Can be biased toward features with more levels (unless regularized or pruned).

**Extensions / improvements:** Pruning, ensemble methods (bagging, boosting), random forests, etc.

### 2.7 Ensemble Methods: Bagging, Random Forests, Boosting

**Ensembles** combine multiple models to produce better performance than any single one.

#### Bagging (Bootstrap Aggregation)
- Create multiple bootstrap samples (resampling with replacement) of the training data.
- Train a base model (e.g. decision tree) on each bootstrap sample.
- Aggregate their predictions (e.g. majority vote for classification, average for regression).

**Random Forest** is a special kind of bagging where each tree also considers only a random subset of features at each split to reduce correlation among trees.

#### Boosting
- Sequentially train models so that each new model focuses on the errors (residuals) of the prior models.
- Models are weighted and combined (often in a weighted sum).
- Examples: AdaBoost, Gradient Boosting Machines (GBMs), XGBoost, LightGBM, etc.

**Notes:**
- Boosting often yields high accuracy but is more prone to overfitting and more sensitive to hyperparameter tuning.

### 2.8 Neural Networks / Deep Learning

**What:** Modeled loosely after the brain, neural networks consist of nodes (“neurons”) arranged in layers. Each neuron computes a weighted sum of inputs, applies an activation function, and passes output to the next layer.

**Key elements:**
- Input layer, hidden layers, output layer.
- Activation functions (sigmoid, ReLU, tanh, etc.).
- Backpropagation algorithm to compute gradients.
- Optimization (e.g. stochastic gradient descent, Adam).

**Deep Learning** means using many hidden layers — enabling learning of hierarchical, high-level features.

**Strengths:**
- Very powerful for complex tasks (image recognition, natural language processing, speech, etc.).
- Can automatically learn features (less need for manual feature engineering).

**Challenges / Caveats:**
- Requires large amounts of data.
- Computationally expensive (GPU acceleration often needed).
- Risk of overfitting, vanishing / exploding gradients.
- Many hyperparameters to tune (layers, neurons, learning rate, regularization).

---

## 3. Unsupervised Learning Algorithms

After covering supervised methods, the video shifts back to unsupervised methods (clustering, dimensionality reduction) to round off the survey.

### 3.1 Clustering / K-means

**What:** Partition the data into \(k\) clusters such that items within a cluster are more similar to each other than to items in other clusters.

**K-means algorithm:**
1. Initialize \(k\) centroids (often randomly).
2. Assign each point to the nearest centroid.
3. Recompute centroids (mean of assigned points).
4. Repeat assignment + update until convergence (no change or minimal change).

**Strengths:**
- Simple, intuitive, scalable.

**Weaknesses / caveats:**
- You need to specify \(k\) in advance.
- Sensitive to initial centroid placement.
- Sensitive to outliers.
- Works best with spherical / equally sized clusters; struggles with irregular shapes or varying densities.

### 3.2 Dimensionality Reduction / PCA (Principal Component Analysis)

**What:** Reduce the number of features while preserving as much variance as possible. Project high-dimensional data into a lower-dimensional subspace.

**PCA process:**
1. Center the data (subtract mean).
2. Compute covariance matrix.
3. Compute eigenvectors + eigenvalues (principal components).
4. Choose top components (by eigenvalue magnitude) to project data onto.

**Use cases:**
- Feature compression / reduction.
- Visualization (e.g. project to 2 or 3 dimensions).
- Noise reduction, dimension elimination.

**Caveats:**
- PCA is linear – it can’t capture nonlinear structure.
- The principal components are orthogonal directions in the original feature space, which may or may not align with meaningful features.
- One must center / standardize data beforehand to avoid biases.

---

## 4. How to Choose Which Algorithm to Use (Insights / Heuristics)

- **Nature of the problem:** Is it regression, classification, clustering, or dimensionality reduction?
- **Size and dimensionality of data:** Some algorithms scale better (e.g. linear regression, Naive Bayes) than others (SVM, neural nets).
- **Linearity vs non-linearity:** If relationships are roughly linear, simpler models (linear / logistic regression) might suffice.
- **Interpretability:** If you need model interpretability, consider decision trees or interpretable linear models.
- **Overfitting / generalization:** More complex models risk overfitting if you don’t have much data.
- **Computational resources:** Neural networks / large SVMs may require more compute / memory.
- **Hyperparameter tuning:** Some methods require careful cross-validation (boosting, SVM, neural nets).
- **Domain knowledge:** Feature selection and engineering often matter more than the choice of model.

---

## 5. Additional Notes, Limitations, and Further Topics

- **Bias–Variance tradeoff:** Simpler models tend to underfit (high bias), complex models overfit (high variance).
- **Regularization:** Techniques like L1 (Lasso), L2 (Ridge), dropout (for neural nets) prevent overfitting.
- **Cross-validation:** Ensures reliable model evaluation.
- **Feature engineering:** Often more impactful than changing algorithms.
- **Data preprocessing:** Includes normalization, standardization, outlier handling, encoding categorical variables.
- **Ensemble stacking:** Combines different models using a meta-learner.
- **Other ML methods:** hierarchical clustering, DBSCAN, t-SNE, autoencoders, GANs, reinforcement learning (Q-learning, MDPs).
- **Scalability:** Big data requires scalable / online algorithms.
- **Interpretability & fairness:** Increasingly important for real-world ML applications.
