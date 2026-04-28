```json
{
  "EML": {

    "role": "semantic perception transform layer",

    "core_principle": {
      "invariance": "does not modify TVA variables (delta_s, lambda, W_c)",
      "function": "transforms interpretation signals only"
    },

    "inputs": {
      "delta_s": "TVA alignment score ∈ [0,1]",
      "U": "uncertainty / instability ∈ [0,1]",
      "context": "optional embedding or state vector"
    },

    "core_transform": {

      "exp_component": {
        "E": "exp(-α · delta_s)",
        "purpose": "compress high misalignment sensitivity"
      },

      "log_component": {
        "L": "log(1 + β · U)",
        "purpose": "expand low-to-mid uncertainty sensitivity"
      },

      "fusion": {
        "S_raw": "E - L"
      },

      "normalization": {
        "S_sem": "sigmoid(S_raw)",
        "range": "[0,1]"
      }
    },

    "outputs": {

      "S_sem": {
        "meaning": "semantic reinforcement signal",
        "type": "interpretation weight"
      },

      "U_modulated": {
        "meaning": "stabilized uncertainty signal",
        "type": "attention depth driver"
      }
    },

    "interface_contract": {

      "allowed_effects": [
        "attention weighting",
        "monitoring depth adjustment",
        "memory salience modulation"
      ],

      "forbidden_effects": [
        "no modification of TVA delta_s",
        "no modification of lambda",
        "no modification of W_c",
        "no control decisions",
        "no state evolution influence"
      ]
    },

    "behavioral_properties": {

      "bounded_output": true,
      "no_feedback_to_TVA": true,
      "stable_under_high_U": true,
      "compression_under_high_delta_s": true
    }
  }
}
```