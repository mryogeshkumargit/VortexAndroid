package com.vortexai.android.ui.screens.settings.managers

import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.booleanPreferencesKey
import com.vortexai.android.ui.screens.settings.SettingsUiState
import com.vortexai.android.domain.service.ImageGenerationService
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ImageSettingsManager @Inject constructor(
    private val settingsDataStore: SettingsDataStore,
    private val imageGenerationService: ImageGenerationService
) {
    suspend fun loadImageSettings(currentState: SettingsUiState): SettingsUiState {
        val preferences = settingsDataStore.getPreferences()
        
        val replicateModel = preferences[SettingsDataStore.REPLICATE_MODEL_KEY] ?: ""
        
        return currentState.copy(
            imageProvider = preferences[SettingsDataStore.IMAGE_PROVIDER_KEY] ?: "Together AI",
            imageSize = preferences[SettingsDataStore.IMAGE_SIZE_KEY] ?: "1024x1024",
            imageQuality = preferences[stringPreferencesKey("image_quality")] ?: "Standard",
            imageModel = preferences[SettingsDataStore.IMAGE_MODEL_KEY] ?: "",
            steps = preferences[SettingsDataStore.STEPS_KEY] ?: 20,
            guidanceScale = preferences[SettingsDataStore.GUIDANCE_SCALE_KEY] ?: 7.5f,
            togetherAiImageApiKey = preferences[SettingsDataStore.TOGETHER_AI_IMAGE_API_KEY] ?: "",
            huggingFaceImageApiKey = preferences[SettingsDataStore.HUGGINGFACE_IMAGE_API_KEY] ?: "",
            modelsLabImageApiKey = preferences[SettingsDataStore.MODELSLAB_IMAGE_API_KEY] ?: "",
            grokImageApiKey = preferences[stringPreferencesKey("grok_image_api_key")] ?: "",
            customImageApiKey = preferences[SettingsDataStore.CUSTOM_IMAGE_API_KEY] ?: "",
            customImageEndpoint = preferences[SettingsDataStore.CUSTOM_IMAGE_ENDPOINT_KEY] ?: "",
            customImageApiPrefix = preferences[SettingsDataStore.CUSTOM_IMAGE_API_PREFIX_KEY] ?: "/v1",
            comfyUiEndpoint = preferences[SettingsDataStore.COMFYUI_ENDPOINT_KEY] ?: "",
            comfyUiWorkflow = preferences[SettingsDataStore.COMFYUI_WORKFLOW_KEY] ?: "SDXL",
            negativePrompt = preferences[SettingsDataStore.NEGATIVE_PROMPT_KEY] ?: "",
            replicateApiKey = preferences[SettingsDataStore.REPLICATE_API_KEY] ?: "",
            replicateModel = replicateModel,
            replicateDisableSafetyChecker = preferences[booleanPreferencesKey("replicate_disable_safety_checker")] ?: false,
            replicateNegativePrompt = preferences[stringPreferencesKey("replicate_negative_prompt")] ?: "",
            replicateWidth = preferences[intPreferencesKey("replicate_width")] ?: 1024,
            replicateHeight = preferences[intPreferencesKey("replicate_height")] ?: 1024,
            useLora = preferences[SettingsDataStore.USE_LORA_KEY] ?: false,
            manuallyAddedImageModels = preferences[stringPreferencesKey("manually_added_image_models")]?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
            manuallyAddedLoraModels = preferences[stringPreferencesKey("manually_added_lora_models")]?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
            manuallyAddedTogetherAiImageModels = preferences[stringPreferencesKey("manually_added_together_ai_image_models")]?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
            manuallyAddedHuggingFaceImageModels = preferences[stringPreferencesKey("manually_added_huggingface_image_models")]?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
            manuallyAddedCustomImageModels = preferences[stringPreferencesKey("manually_added_custom_image_models")]?.split(",")?.filter { it.isNotBlank() } ?: emptyList(),
            selectedCustomImageProviderId = preferences[stringPreferencesKey("selected_custom_image_provider_id")] ?: "",
            selectedCustomImageEditProviderId = preferences[stringPreferencesKey("selected_custom_image_edit_provider_id")] ?: "",
            imageEditingProvider = preferences[stringPreferencesKey("image_editing_provider")] ?: "Together AI",
            comfyUiEditingEndpoint = preferences[stringPreferencesKey("comfyui_editing_endpoint")] ?: "",
            comfyUiEditingWorkflow = preferences[stringPreferencesKey("comfyui_editing_workflow")] ?: "",
            comfyUiEditingCheckpoint = preferences[stringPreferencesKey("comfyui_editing_checkpoint")] ?: "",
            comfyUiEditingLora = preferences[stringPreferencesKey("comfyui_editing_lora")] ?: "",
            comfyUiEditingLoraStrength = preferences[androidx.datastore.preferences.core.floatPreferencesKey("comfyui_editing_lora_strength")] ?: 1.0f,
            comfyUiEditingUseLora = preferences[androidx.datastore.preferences.core.booleanPreferencesKey("comfyui_editing_use_lora")] ?: false,
            comfyUiCustomWorkflow = preferences[stringPreferencesKey("comfyui_custom_workflow")] ?: "",
            comfyUiNegativePrompt = preferences[stringPreferencesKey("comfyui_negative_prompt")] ?: "",
            comfyUiWorkflowFileName = preferences[stringPreferencesKey("comfyui_workflow_filename")] ?: "",
            replicateEditingApiKey = preferences[stringPreferencesKey("replicate_editing_api_key")] ?: "",
            replicateEditingModel = preferences[stringPreferencesKey("replicate_editing_model")] ?: "qwen-image-edit",
            togetherAiEditingApiKey = preferences[stringPreferencesKey("together_ai_editing_api_key")] ?: "",
            imageEditingModel = preferences[stringPreferencesKey("image_editing_model")] ?: "black-forest-labs/FLUX.1-kontext-dev",
            imageEditingStrength = preferences[stringPreferencesKey("image_editing_strength")] ?: "Medium (0.5)",
            modelslabEditingApiKey = preferences[stringPreferencesKey("modelslab_editing_api_key")] ?: "",
            modelslabEditingModel = preferences[stringPreferencesKey("modelslab_editing_model")] ?: "flux-kontext-dev",
            modelslabEditingStrength = preferences[stringPreferencesKey("modelslab_editing_strength")] ?: "High (0.7)",
            modelslabEditingStrengthFloat = preferences[androidx.datastore.preferences.core.floatPreferencesKey("modelslab_editing_strength_float")] ?: 0.7f,
            imgbbApiKey = preferences[stringPreferencesKey("imgbb_api_key")] ?: "",
            modelslabNegativePrompt = preferences[stringPreferencesKey("modelslab_negative_prompt")] ?: "(worst quality:2), (low quality:2), (normal quality:2), (jpeg artifacts), (blurry), (duplicate), (morbid), (mutilated), (out of frame), (extra limbs), (bad anatomy), (disfigured), (deformed), (cross-eye), (glitch), (oversaturated), (overexposed), (underexposed), (bad proportions), (bad hands), (bad feet), (cloned face), (long neck), (missing arms), (missing legs), (extra fingers), (fused fingers), (poorly drawn hands), (poorly drawn face), (mutation), (deformed eyes), watermark, text, logo, signature, grainy, tiling, censored, nsfw, ugly, blurry eyes, noisy image, bad lighting, unnatural skin, asymmetry"
        )
    }

    suspend fun saveImageSettings(state: SettingsUiState) {
        settingsDataStore.savePreferences { preferences: androidx.datastore.preferences.core.MutablePreferences ->
            preferences[SettingsDataStore.IMAGE_PROVIDER_KEY] = state.imageProvider
            preferences[SettingsDataStore.IMAGE_SIZE_KEY] = state.imageSize
            preferences[stringPreferencesKey("image_quality")] = state.imageQuality
            preferences[SettingsDataStore.IMAGE_MODEL_KEY] = state.imageModel
            preferences[SettingsDataStore.STEPS_KEY] = state.steps
            preferences[SettingsDataStore.GUIDANCE_SCALE_KEY] = state.guidanceScale
            preferences[SettingsDataStore.TOGETHER_AI_IMAGE_API_KEY] = state.togetherAiImageApiKey
            preferences[SettingsDataStore.HUGGINGFACE_IMAGE_API_KEY] = state.huggingFaceImageApiKey
            preferences[SettingsDataStore.MODELSLAB_IMAGE_API_KEY] = state.modelsLabImageApiKey
            preferences[stringPreferencesKey("grok_image_api_key")] = state.grokImageApiKey
            preferences[SettingsDataStore.CUSTOM_IMAGE_API_KEY] = state.customImageApiKey
            preferences[SettingsDataStore.CUSTOM_IMAGE_ENDPOINT_KEY] = state.customImageEndpoint
            preferences[SettingsDataStore.CUSTOM_IMAGE_API_PREFIX_KEY] = state.customImageApiPrefix
            preferences[SettingsDataStore.COMFYUI_ENDPOINT_KEY] = state.comfyUiEndpoint
            preferences[SettingsDataStore.COMFYUI_WORKFLOW_KEY] = state.comfyUiWorkflow
            preferences[SettingsDataStore.NEGATIVE_PROMPT_KEY] = state.negativePrompt
            preferences[SettingsDataStore.USE_LORA_KEY] = state.useLora
            preferences[SettingsDataStore.REPLICATE_API_KEY] = state.replicateApiKey
            preferences[SettingsDataStore.REPLICATE_MODEL_KEY] = state.replicateModel
            preferences[booleanPreferencesKey("replicate_disable_safety_checker")] = state.replicateDisableSafetyChecker
            preferences[stringPreferencesKey("replicate_negative_prompt")] = state.replicateNegativePrompt
            preferences[intPreferencesKey("replicate_width")] = state.replicateWidth
            preferences[intPreferencesKey("replicate_height")] = state.replicateHeight
            preferences[stringPreferencesKey("manually_added_image_models")] = state.manuallyAddedImageModels.joinToString(",")
            preferences[stringPreferencesKey("manually_added_lora_models")] = state.manuallyAddedLoraModels.joinToString(",")
            preferences[stringPreferencesKey("manually_added_together_ai_image_models")] = state.manuallyAddedTogetherAiImageModels.joinToString(",")
            preferences[stringPreferencesKey("manually_added_huggingface_image_models")] = state.manuallyAddedHuggingFaceImageModels.joinToString(",")
            preferences[stringPreferencesKey("manually_added_custom_image_models")] = state.manuallyAddedCustomImageModels.joinToString(",")
            preferences[stringPreferencesKey("selected_custom_image_provider_id")] = state.selectedCustomImageProviderId
            preferences[stringPreferencesKey("selected_custom_image_edit_provider_id")] = state.selectedCustomImageEditProviderId
        }
    }

    suspend fun fetchImageModels(provider: String, apiKey: String, customEndpoint: String?, manualModels: List<String>): Result<List<String>> {
        return try {
            val result = imageGenerationService.fetchAvailableModels(provider, apiKey, customEndpoint, manualModels)
            result
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun fetchLoraModels(provider: String, apiKey: String, customEndpoint: String?, manualModels: List<String>): Result<List<String>> {
        return try {
            val result = imageGenerationService.fetchLoraModels(provider, apiKey, customEndpoint, manualModels)
            result
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun fetchComfyUiModels(endpoint: String): Result<Pair<List<String>, List<String>>> {
        return try {
            val result = imageGenerationService.fetchComfyUiModels(endpoint)
            result
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}