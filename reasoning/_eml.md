```json
{
  "EML": {

    "role": "Exp-Minus-Log semantic perception transform layer for Metacognition",

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
        "no modification of delta_s",
        "no modification of lambda",
        "no modification of W_c",
        "no state evolution influence"
      ]
    },

    "behavioral_properties": {

      "bounded_output": true,
      "stable_under_high_U": true,
      "compression_under_high_delta_s": true
    }
  }
}
```