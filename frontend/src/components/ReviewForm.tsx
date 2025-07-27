import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import RatingStars from './RatingStars';
import { useReviewStore } from '../store/reviewStore';
import { CreateReviewForm } from '../types';

const ReviewForm: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const { createReview, loading } = useReviewStore();

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
    reset,
  } = useForm<CreateReviewForm>({
    defaultValues: {
      rating: 5,
    },
  });

  const watchContent = watch('content', '');
  const watchRating = watch('rating', 5);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast.error('Bild ist zu groß. Maximum: 5MB');
        return;
      }

      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedFile(null);
    setImagePreview(null);
  };

  const onSubmit = async (data: CreateReviewForm) => {
    const formData = {
      ...data,
      image: selectedFile || undefined,
    };

    const success = await createReview(formData);
    
    if (success) {
      toast.success('Bewertung erfolgreich erstellt!');
      reset();
      setSelectedFile(null);
      setImagePreview(null);
    } else {
      toast.error('Fehler beim Erstellen der Bewertung');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Name */}
      <div>
        <label htmlFor="name" className="form-label">
          Name *
        </label>
        <input
          id="name"
          type="text"
          className={`form-input ${errors.name ? 'border-red-500' : ''}`}
          {...register('name', {
            required: 'Name ist erforderlich',
            minLength: { value: 2, message: 'Name muss mindestens 2 Zeichen haben' },
          })}
        />
        {errors.name && (
          <p className="form-error">{errors.name.message}</p>
        )}
      </div>

      {/* E-Mail (optional) */}
      <div>
        <label htmlFor="email" className="form-label">
          E-Mail (optional)
        </label>
        <input
          id="email"
          type="email"
          className={`form-input ${errors.email ? 'border-red-500' : ''}`}
          {...register('email', {
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Ungültige E-Mail-Adresse',
            },
          })}
        />
        {errors.email && (
          <p className="form-error">{errors.email.message}</p>
        )}
      </div>

      {/* Bewertung */}
      <div>
        <label className="form-label">Bewertung *</label>
        <RatingStars
          rating={watchRating}
          interactive
          onChange={(rating) => setValue('rating', rating)}
        />
      </div>

      {/* Titel (optional) */}
      <div>
        <label htmlFor="title" className="form-label">
          Titel (optional)
        </label>
        <input
          id="title"
          type="text"
          className="form-input"
          placeholder="Zusammenfassung Ihrer Erfahrung"
          {...register('title', {
            maxLength: { value: 200, message: 'Titel zu lang (max. 200 Zeichen)' },
          })}
        />
        {errors.title && (
          <p className="form-error">{errors.title.message}</p>
        )}
      </div>

      {/* Bewertungstext */}
      <div>
        <label htmlFor="content" className="form-label">
          Bewertung *
        </label>
        <textarea
          id="content"
          rows={6}
          className={`form-textarea ${errors.content ? 'border-red-500' : ''}`}
          placeholder="Beschreiben Sie Ihre Erfahrung..."
          {...register('content', {
            required: 'Bewertungstext ist erforderlich',
            minLength: { value: 10, message: 'Bewertung muss mindestens 10 Zeichen haben' },
            maxLength: { value: 5000, message: 'Bewertung zu lang (max. 5000 Zeichen)' },
          })}
        />
        <div className={`char-counter ${
          watchContent.length > 4500 
            ? 'error' 
            : watchContent.length > 4000 
              ? 'warning' 
              : ''
        }`}>
          {watchContent.length}/5000 Zeichen
        </div>
        {errors.content && (
          <p className="form-error">{errors.content.message}</p>
        )}
      </div>

      {/* Bild-Upload */}
      <div>
        <label className="form-label">Bild (optional)</label>
        
        {!imagePreview ? (
          <div className="image-upload-area">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
              id="image-upload"
            />
            <label htmlFor="image-upload" className="cursor-pointer">
              <div className="flex flex-col items-center">
                <svg
                  className="w-8 h-8 text-gray-400 mb-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <p className="text-sm text-gray-600">
                  Klicken Sie hier, um ein Bild hochzuladen
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  PNG, JPG, GIF bis 5MB
                </p>
              </div>
            </label>
          </div>
        ) : (
          <div className="relative">
            <img
              src={imagePreview}
              alt="Vorschau"
              className="w-full h-48 object-cover rounded-lg border border-gray-300"
            />
            <button
              type="button"
              onClick={removeImage}
              className="absolute top-2 right-2 bg-red-600 text-white rounded-full p-1 hover:bg-red-700 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}
      </div>

      {/* Submit Button */}
      <div>
        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full flex justify-center items-center"
        >
          {loading ? (
            <>
              <div className="spinner mr-2" />
              Wird gesendet...
            </>
          ) : (
            'Bewertung abgeben'
          )}
        </button>
      </div>
    </form>
  );
};

export default ReviewForm;
