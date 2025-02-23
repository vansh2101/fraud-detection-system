import torch
import cv2
import numpy as np
from PIL import Image
from transformers import (
    VisionEncoderDecoderModel, 
    ViTFeatureExtractor, 
    AutoTokenizer,
    BartForConditionalGeneration, 
    BartTokenizer
)

class VideoCaptioner:
    def __init__(self):
        self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.caption_tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

        self.summary_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        self.summary_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.caption_model.to(self.device)
        self.summary_model.to(self.device)

        self.max_length = 50  
        self.num_beams = 15  
        self.gen_kwargs = {
            "max_length": self.max_length, 
            "num_beams": self.num_beams,
            "no_repeat_ngram_size": 2, 
            "early_stopping": True
        }

    def extract_diverse_frames(self, video_path, max_frames=30):
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps
        
        frame_indices = []
        if total_frames <= max_frames:
            # If fewer frames than max, use all
            frame_indices = list(range(total_frames))
        else:
            # Select frames across different segments of the video
            segment_size = total_frames // max_frames
            for i in range(max_frames):
                # Select a frame from each segment, with some randomness
                base_index = i * segment_size
                random_offset = np.random.randint(0, segment_size)
                frame_index = base_index + random_offset
                frame_indices.append(min(frame_index, total_frames - 1))
        
        # Extract selected frames
        selected_frames = []
        for index in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = cap.read()
            if ret:
                # Convert OpenCV BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                selected_frames.append(pil_image)
        
        cap.release()
        return selected_frames

    def generate_enhanced_captions(self, frames):
        # Prepare frames
        pixel_values = self.feature_extractor(images=frames, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)
        
        # Generate captions with enhanced parameters
        output_ids = self.caption_model.generate(
            pixel_values, 
            **self.gen_kwargs,
            temperature=0.8, 
            top_k=50,
            top_p=0.95
        )
        
        # Decode and clean captions
        captions = self.caption_tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        captions = [caption.strip() for caption in captions]
        
        return captions

    def filter_unique_captions(self, captions, similarity_threshold=0.7):
        from difflib import SequenceMatcher
        
        def caption_similarity(caption1, caption2):
            return SequenceMatcher(None, caption1, caption2).ratio()
        
        unique_captions = []
        for caption in captions:
            is_unique = True
            for unique_caption in unique_captions:
                if caption_similarity(caption, unique_caption) > similarity_threshold:
                    is_unique = False
                    break
            
            if is_unique:
                unique_captions.append(caption)
        
        return unique_captions

    def summarize_with_context(self, captions):
        # Combine captions with some context preservation
        combined_text = " ".join(captions)
        
        # Prepare inputs with more flexible tokenization
        inputs = self.summary_tokenizer(
            combined_text, 
            max_length=1024, 
            return_tensors="pt", 
            truncation=True,
            padding=True
        )
        
        # Generate summary with enhanced parameters
        summary_ids = self.summary_model.generate(
            inputs.input_ids.to(self.device), 
            num_beams=6, 
            max_length=200, 
            early_stopping=True,
            temperature=0.7, 
            no_repeat_ngram_size=3
        )
        
        # Decode and clean summary
        summary = self.summary_tokenizer.decode(
            summary_ids[0], 
            skip_special_tokens=True
        )
        
        return summary

    def caption_video(self, video_path):
        # Extract diverse frames
        frames = self.extract_diverse_frames(video_path)
        
        # Generate enhanced captions
        frame_captions = self.generate_enhanced_captions(frames)
        
        # Filter unique captions
        unique_captions = self.filter_unique_captions(frame_captions)
        
        # Generate contextual summary
        video_summary = self.summarize_with_context(unique_captions)
        
        return {
            "frame_count": len(frames),
            "frame_captions": unique_captions,
            "video_summary": video_summary
        }