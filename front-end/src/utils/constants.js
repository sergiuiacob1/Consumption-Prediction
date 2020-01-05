export const MODEL_FIELDS = [
  { key: 'optimizer', name: 'Optimizer', type: 'text', defaultValue: 'adam'},
  { key: 'learning_rate', name: 'Learning rate', type: 'number', defaultValue: 0.01},
  { key: 'learning_rate_decay', name: 'Learning rate decay', type: 'number', defaultValue: 0.000001},
  { key: 'epochs', name: 'Epochs', type: 'number', defaultValue: 100},
  { key: 'hidden_layer_sizes', name: 'Hidden layer sizes (list)', type: 'text', defaultValue: [100, 10]},
  { key: 'layer_activations', name: 'Layer activations', type: 'text', defaultValue: ['relu', 'relu']},
  { key: 'layer_dropout_values', name: 'Layer dropout values', type: 'text', defaultValue: [0.25, 0.0]},
  { key: 'weight_initializers', name: 'Weight initializers', type: 'text', defaultValue: ['normal', 'normal']},
  { key: 'batch_size', name: 'Batch size', type: 'number', defaultValue: 16},
]