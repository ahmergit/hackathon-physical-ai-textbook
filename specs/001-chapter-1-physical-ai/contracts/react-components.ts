/**
 * React Component Contracts for Chapter 1 - Physical AI
 *
 * This file defines TypeScript interfaces for all React components used in
 * Chapter 1 lessons. These are contracts, not implementations.
 *
 * Implementation location: book-source/src/components/
 */

// =============================================================================
// Summary Button Component
// =============================================================================

/**
 * Props for the SummaryButton component.
 *
 * Displays an AI-generated summary of the lesson content when clicked.
 * Initially uses mock data; future versions may integrate with RAG assistant.
 */
export interface SummaryButtonProps {
  /**
   * Unique identifier for the lesson.
   * Format: "lesson-{NN}" where NN is zero-padded number (01-99).
   * Example: "lesson-01", "lesson-02"
   */
  lessonId: string;

  /**
   * Custom button text.
   * Default: "AI Summary"
   */
  title?: string;

  /**
   * Additional CSS classes for styling.
   */
  className?: string;

  /**
   * Icon to display on button.
   * Default: "✨" (sparkles emoji)
   */
  icon?: string;
}

/**
 * State interface for SummaryButton component.
 */
export interface SummaryButtonState {
  /**
   * Whether the summary panel is currently visible.
   */
  isOpen: boolean;

  /**
   * The generated summary text.
   * Null if not yet generated.
   */
  summary: string | null;

  /**
   * Loading state while generating summary.
   */
  isLoading: boolean;

  /**
   * Error message if summary generation fails.
   */
  error: string | null;
}

/**
 * Mock summary data structure.
 * Used until real AI integration is available.
 */
export interface LessonSummary {
  lessonId: string;
  summary: string;
  keyPoints: string[];
  readingTime: number; // in minutes
}

// =============================================================================
// Personalize Button Component
// =============================================================================

/**
 * Props for the PersonalizeButton component.
 *
 * Allows users to adapt lesson content to their skill level.
 * Displays a dropdown or button group for level selection.
 */
export interface PersonalizeButtonProps {
  /**
   * Unique identifier for the lesson.
   * Format: "lesson-{NN}" where NN is zero-padded number (01-99).
   * Example: "lesson-01", "lesson-02"
   */
  lessonId: string;

  /**
   * Available skill levels for personalization.
   * Default: ["Beginner", "Intermediate", "Advanced"]
   */
  levels?: SkillLevel[];

  /**
   * Default selected level.
   * Default: "Beginner"
   */
  defaultLevel?: SkillLevel;

  /**
   * Additional CSS classes for styling.
   */
  className?: string;

  /**
   * Callback fired when level changes.
   * Allows parent components to react to level changes.
   */
  onLevelChange?: (level: SkillLevel) => void;
}

/**
 * State interface for PersonalizeButton component.
 */
export interface PersonalizeButtonState {
  /**
   * Currently selected skill level.
   */
  selectedLevel: SkillLevel;

  /**
   * Whether content is currently personalized.
   */
  isPersonalized: boolean;

  /**
   * Whether dropdown menu is open.
   */
  isMenuOpen: boolean;
}

/**
 * Skill level enum.
 */
export type SkillLevel = "Beginner" | "Intermediate" | "Advanced";

/**
 * Personalization configuration for a lesson.
 * Defines how content adapts to each skill level.
 */
export interface PersonalizationConfig {
  lessonId: string;
  levels: {
    [K in SkillLevel]: {
      /**
       * Suggested reading time for this level.
       */
      readingTime: number; // in minutes

      /**
       * Additional context or explanations for this level.
       */
      additionalContext?: string;

      /**
       * Sections to highlight or emphasize for this level.
       */
      highlightSections?: string[]; // section IDs

      /**
       * Suggested next steps or resources for this level.
       */
      nextSteps?: string[];
    };
  };
}

// =============================================================================
// Expert Insight Component (Optional Custom Admonition)
// =============================================================================

/**
 * Props for custom Expert Insight component.
 *
 * This is OPTIONAL - default implementation uses Docusaurus admonitions (:::tip).
 * Only needed if custom styling or behavior is required.
 */
export interface ExpertInsightProps {
  /**
   * The insight content (markdown supported).
   */
  children: React.ReactNode;

  /**
   * Optional title for the insight box.
   * Default: "Expert Insight"
   */
  title?: string;

  /**
   * Variant of the insight box.
   * Default: "tip"
   */
  variant?: "tip" | "info" | "note";

  /**
   * Optional author attribution.
   */
  author?: string;

  /**
   * Additional CSS classes for styling.
   */
  className?: string;
}

// =============================================================================
// Visual Aid Component (For Diagrams/Images)
// =============================================================================

/**
 * Props for diagram or image captions.
 */
export interface VisualAidProps {
  /**
   * Figure number (e.g., 1, 2, 3).
   * Used for automatic numbering and cross-references.
   */
  figureNumber: number;

  /**
   * Caption text describing the visual.
   */
  caption: string;

  /**
   * Type of visual aid.
   */
  type: "diagram" | "image" | "chart";

  /**
   * Alt text for accessibility.
   * Required for images and charts.
   */
  altText?: string;

  /**
   * Image source path.
   * Required for type="image".
   */
  src?: string;

  /**
   * Mermaid diagram code.
   * Required for type="diagram".
   */
  mermaidCode?: string;

  /**
   * Additional CSS classes for styling.
   */
  className?: string;
}

// =============================================================================
// Lesson Metadata (For SEO and Navigation)
// =============================================================================

/**
 * Frontmatter structure for lesson markdown files.
 */
export interface LessonFrontmatter {
  /**
   * Position in sidebar.
   * Must be unique within chapter.
   */
  sidebar_position: number;

  /**
   * Meta description for SEO.
   * Max 160 characters.
   */
  description?: string;

  /**
   * Keywords for SEO.
   */
  keywords?: string[];

  /**
   * Custom URL slug.
   * Default: derived from filename.
   */
  slug?: string;

  /**
   * Custom title for sidebar.
   * Default: H1 heading from content.
   */
  title?: string;

  /**
   * Estimated reading time in minutes.
   * Auto-calculated if not provided.
   */
  reading_time?: number;

  /**
   * Lesson number within chapter.
   * Example: 1, 2, 3, 4, 5
   */
  lesson_number?: number;

  /**
   * Prerequisite lessons.
   * Array of lesson IDs that should be read first.
   */
  prerequisites?: string[];
}

// =============================================================================
// Category Configuration (For Parts and Chapters)
// =============================================================================

/**
 * Category configuration for _category_.json files.
 */
export interface CategoryConfig {
  /**
   * Human-readable label for the category.
   * Max 80 characters.
   */
  label: string;

  /**
   * Position in sidebar.
   * Must be unique within parent.
   */
  position: number;

  /**
   * Whether category can be collapsed.
   */
  collapsible: boolean;

  /**
   * Default collapsed state.
   */
  collapsed: boolean;

  /**
   * Optional link configuration.
   */
  link?: {
    /**
     * Link type.
     */
    type: "generated-index" | "doc";

    /**
     * Description for generated index pages.
     */
    description?: string;

    /**
     * Document ID for type="doc".
     */
    id?: string;
  };

  /**
   * Custom class name for styling.
   */
  className?: string;

  /**
   * Custom label for collapsed state.
   */
  collapsedLabel?: string;
}

// =============================================================================
// Component API Validation
// =============================================================================

/**
 * Validation rules for component props.
 */
export const ComponentValidation = {
  SummaryButton: {
    lessonId: {
      pattern: /^lesson-(0[1-9]|[1-9][0-9])$/,
      message: 'lessonId must match pattern "lesson-{NN}" where NN is 01-99',
    },
    title: {
      maxLength: 30,
      message: "title must not exceed 30 characters",
    },
  },

  PersonalizeButton: {
    lessonId: {
      pattern: /^lesson-(0[1-9]|[1-9][0-9])$/,
      message: 'lessonId must match pattern "lesson-{NN}" where NN is 01-99',
    },
    levels: {
      allowedValues: ["Beginner", "Intermediate", "Advanced"],
      message: 'levels must be one of: "Beginner", "Intermediate", "Advanced"',
    },
  },

  LessonFrontmatter: {
    sidebar_position: {
      min: 1,
      max: 99,
      message: "sidebar_position must be between 1 and 99",
    },
    description: {
      maxLength: 160,
      message: "description must not exceed 160 characters",
    },
  },

  CategoryConfig: {
    label: {
      maxLength: 80,
      message: "label must not exceed 80 characters",
    },
    position: {
      min: 1,
      max: 99,
      message: "position must be between 1 and 99",
    },
  },
} as const;

// =============================================================================
// Export All Interfaces
// =============================================================================

export type {
  SummaryButtonProps,
  SummaryButtonState,
  LessonSummary,
  PersonalizeButtonProps,
  PersonalizeButtonState,
  SkillLevel,
  PersonalizationConfig,
  ExpertInsightProps,
  VisualAidProps,
  LessonFrontmatter,
  CategoryConfig,
};
