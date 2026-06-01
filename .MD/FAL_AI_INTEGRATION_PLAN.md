# fal.ai Integration Implementation Plan

## Current Status Assessment

### ✅ Phase 1 & 2: ALREADY COMPLETE
The Settings architecture has already been refactored using the Manager pattern:
- `InterfaceSettingsManager`
- `LLMSettingsManager`
- `ImageSettingsManager`
- `AudioSettingsManager`
- `BackupSettingsManager`
- `ModelCacheManager`

The SettingsViewModel is now ~1000 lines (down from 2000+) and delegates to specialized managers.

### 🔄 Phase 3: fal.ai Backend Integration (IN PROGRESS)

#### Existing fal.ai Infrastructure
1. **LLM Provider**: `FalAILLMProvider.kt` - ✅ Already implemented
2. **Custom API Configs**: Multiple JSON configs in `CustomAPIs/` folder
   - `fal_ai_flux_2_pro.json`
   - `fal_ai_flux_pro_v1_1.json`
   - `fal_ai_gpt_image_1_5_edit.json`
   - `fal_ai_nano_banana_pro.json`
   - `fal_ai_nano_banana_pro_edit.json`

3. **Video Generation**: Already uses fal.ai (see `falAiVideoApiKey` in SettingsUiState)

#### What Needs to be Done

### A. Unified API Key Migration
**Current State**: 
- `falAiVideoApiKey` exists for video
- No unified `falAiApiKey` for all services

**Action Required**:
1. Add `falAiApiKey` to SettingsUiState (already exists!)
2. Migrate video settings to use unified key
3. Add fal.ai as a first-class provider option (not just Custom API)

### B. LLM Integration
**Status**: ✅ Provider exists, needs UI integration

**Tasks**:
1. Add "fal.ai" to LLM provider dropdown in `LLMConfigurationTab`
2. Wire up `FalAILLMProvider` in `ChatLLMService`
3. Add model selection UI for fal.ai models:
   - `fal-ai/any-llm` (default)
   - `fal-ai/meta-llama/Meta-Llama-3-70B-Instruct`
   - Other supported models

### C. Image Generation Integration
**Status**: ⚠️ Placeholder exists, needs implementation

**Current Code** (ImageGenerationService.kt):
```kotlin
private suspend fun generateWithFalAI(
    apiKey: String,
    request: ImageGenerationRequest,
    generationId: String
): Result<ImageGenerationResult>
```

**Tasks**:
1. Implement async queue polling (similar to video service)
2. Add fal.ai to image provider dropdown
3. Support models:
   - `fal-ai/flux-pro`
   - `fal-ai/flux-dev`
   - `fal-ai/flux-schnell`
   - `fal-ai/flux-pro/v1.1`

**Implementation Pattern**:
```kotlin
// 1. Submit to queue
val queueUrl = "https://queue.fal.run/${model}"
val submitResponse = submitToQueue(queueUrl, apiKey, request)

// 2. Poll for completion
val requestId = submitResponse.request_id
val statusUrl = "https://queue.fal.run/${model}/requests/${requestId}/status"
pollUntilComplete(statusUrl, apiKey)

// 3. Fetch result
val resultUrl = "https://queue.fal.run/${model}/requests/${requestId}"
val result = fetchResult(resultUrl, apiKey)
```

### D. Image Editing Integration
**Status**: ❌ Not implemented

**Tasks**:
1. Add fal.ai to image editing provider dropdown
2. Implement in `ImageEditingService.kt`
3. Support models:
   - `fal-ai/flux/dev/image-to-image`
   - `fal-ai/flux-pro/v1.1/redux`
   - `fal-ai/gpt-image-1.5-edit`

**API Pattern**:
```kotlin
fun editImageWithFalAI(
    apiKey: String,
    request: ImageEditingRequest,
    model: String = "fal-ai/flux/dev/image-to-image"
): Result<ImageEditingResult> {
    // Similar queue pattern as image generation
    // But includes image_url or image_base64 in request
}
```

## Implementation Order

### Step 1: Add fal.ai as First-Class Provider (UI)
- [ ] Add "fal.ai" option to LLM provider dropdown
- [ ] Add "fal.ai" option to Image Generation provider dropdown
- [ ] Add "fal.ai" option to Image Editing provider dropdown
- [ ] Add unified API key field in Settings

### Step 2: Complete Image Generation Implementation
- [ ] Implement `generateWithFalAI()` in ImageGenerationService
- [ ] Add queue polling logic
- [ ] Test with FLUX models
- [ ] Add to ImageGenerationTab UI

### Step 3: Implement Image Editing
- [ ] Create `editImageWithFalAI()` in ImageEditingService
- [ ] Support image-to-image workflows
- [ ] Add to ImageEditingTab UI

### Step 4: Testing & Verification
- [ ] Test LLM generation with fal.ai
- [ ] Test image generation with FLUX models
- [ ] Test image editing workflows
- [ ] Verify API key migration from video to unified key

## API Key Migration Strategy

### DataStore Migration
```kotlin
// In SettingsViewModel.init or migration function
viewModelScope.launch {
    val prefs = dataStore.data.first()
    val oldVideoKey = prefs[FAL_AI_VIDEO_API_KEY]
    val newUnifiedKey = prefs[FAL_AI_API_KEY]
    
    // Migrate if unified key is empty but video key exists
    if (newUnifiedKey.isNullOrBlank() && !oldVideoKey.isNullOrBlank()) {
        dataStore.edit { 
            it[FAL_AI_API_KEY] = oldVideoKey
        }
    }
}
```

## UI Changes Required

### LLMConfigurationTab.kt
```kotlin
// Add to provider dropdown
"fal.ai" -> {
    OutlinedTextField(
        value = uiState.falAiApiKey,
        onValueChange = { viewModel.updateFalAiApiKey(it) },
        label = { Text("fal.ai API Key") }
    )
    // Model dropdown for fal.ai models
}
```

### ImageGenerationTab.kt
```kotlin
// Add to provider dropdown
"fal.ai" -> {
    // API key field (shared with LLM)
    // Model selection: flux-pro, flux-dev, flux-schnell
    // Parameters: image_size, num_inference_steps, guidance_scale
}
```

### ImageEditingTab.kt
```kotlin
// Add to provider dropdown
"fal.ai" -> {
    // API key field (shared)
    // Model selection for editing models
    // Strength parameter
}
```

## Testing Checklist

- [ ] LLM: Generate text with fal-ai/any-llm
- [ ] LLM: Generate text with Meta-Llama model
- [ ] Image: Generate with flux-pro
- [ ] Image: Generate with flux-schnell (fast)
- [ ] Image: Edit existing image with flux/dev/image-to-image
- [ ] Video: Verify existing video generation still works
- [ ] Settings: Verify API key is shared across all services
- [ ] Settings: Verify migration from old video key

## Notes

- fal.ai uses `Key {apiKey}` authorization header (not `Bearer`)
- Most endpoints use async queue pattern: submit → poll → fetch
- Image sizes use presets: `square_hd`, `landscape_4_3`, `portrait_16_9`, or `{width}x{height}`
- Default guidance_scale for FLUX: 3.5 (not 7.5 like SD)
- FLUX models are fast: flux-schnell can generate in ~2 seconds

## References

- fal.ai Docs: https://fal.ai/models
- FLUX Pro: https://fal.ai/models/fal-ai/flux-pro
- FLUX Dev: https://fal.ai/models/fal-ai/flux-dev
- Image Editing: https://fal.ai/models/fal-ai/flux/dev/image-to-image
