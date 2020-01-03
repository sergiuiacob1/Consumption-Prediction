export const MODEL_FIELDS = [
  { key: 'learning_rate', name: 'Learning rate', type: 'text', defaultValue: 'constant'},
  { key: 'learning_rate_init', name: 'Learning rate initialization', type: 'number', defaultValue: '0.001'},
  { key: 'max_iter', name: 'Maximum iterations', type: 'number', defaultValue: '200'},
  { key: 'tol', name: 'Learning threshold', type: 'number', defaultValue: '1e-4'},
  { key: 'hidden_layer_sizes', name: 'Hidden layer sizes (list)', type: 'text', defaultValue: '100'},
  { key: 'batch_size', name: 'Batch size', type: 'number', defaultValue: 'auto'},
  { key: 'solver', name: 'Solver', type: 'text', defaultValue: 'adam'},
  { key: 'activaction', name: 'Activation', type: 'text', defaultValue: 'relu'},
]