/**
 * Unit tests for profile page
 * Tests: T091 [US4] - form loads data, submits updates correctly
 *
 * Note: Requires testing libraries to be installed:
 * npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest
 */

/**
 * Once testing libraries are installed, uncomment and use these tests:

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import Profile from '../../src/pages/profile';
import * as api from '../../src/services/api';

jest.mock('../../src/services/api');
jest.mock('../../src/hooks/useAuth', () => ({
  useAuth: () => ({
    isAuthenticated: true,
    user: { email: 'test@example.com', id: '123' },
    loading: false,
  }),
}));

describe('Profile Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('loads existing profile data on mount', async () => {
    const mockProfile = {
      robotics_experience: 'intermediate',
      programming_experience: 'advanced',
      ai_ml_experience: 'beginner',
      learning_goals: 'Build humanoid robots',
      preferred_learning_style: 'hands_on',
      weekly_time_commitment: 15,
    };

    jest.spyOn(api, 'get').mockResolvedValueOnce({ data: mockProfile });

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Build humanoid robots')).toBeInTheDocument();
    });

    // Check that form fields are populated
    expect(screen.getByDisplayValue('intermediate')).toBeInTheDocument();
    expect(screen.getByDisplayValue('advanced')).toBeInTheDocument();
    expect(screen.getByDisplayValue('15')).toBeInTheDocument();
  });

  it('submits updated profile data', async () => {
    const user = userEvent.setup();
    const mockProfile = {
      robotics_experience: 'beginner',
      programming_experience: 'beginner',
      ai_ml_experience: 'none',
      learning_goals: 'Start learning',
      preferred_learning_style: 'visual',
      weekly_time_commitment: 5,
    };

    jest.spyOn(api, 'get').mockResolvedValueOnce({ data: mockProfile });
    const postSpy = jest.spyOn(api, 'post').mockResolvedValueOnce({ data: {} });

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Start learning')).toBeInTheDocument();
    });

    // Update learning goals
    const goalsInput = screen.getByLabelText(/learning goals/i);
    await user.clear(goalsInput);
    await user.type(goalsInput, 'Build advanced robots');

    // Update experience level
    const roboticsSelect = screen.getByLabelText(/robotics experience/i);
    await user.selectOptions(roboticsSelect, 'intermediate');

    // Submit form
    const saveButton = screen.getByRole('button', { name: /save/i });
    await user.click(saveButton);

    // Check API was called with updated data
    await waitFor(() => {
      expect(postSpy).toHaveBeenCalledWith(
        '/profile',
        expect.objectContaining({
          learning_goals: 'Build advanced robots',
          robotics_experience: 'intermediate',
        })
      );
    });
  });

  it('displays success message after save', async () => {
    const user = userEvent.setup();
    const mockProfile = {
      robotics_experience: 'beginner',
      programming_experience: 'beginner',
      ai_ml_experience: 'none',
      learning_goals: 'Test',
      preferred_learning_style: 'visual',
      weekly_time_commitment: 5,
    };

    jest.spyOn(api, 'get').mockResolvedValueOnce({ data: mockProfile });
    jest.spyOn(api, 'post').mockResolvedValueOnce({ data: mockProfile });

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test')).toBeInTheDocument();
    });

    const saveButton = screen.getByRole('button', { name: /save/i });
    await user.click(saveButton);

    // Should show success message
    await waitFor(() => {
      expect(
        screen.getByText(/profile updated successfully/i) ||
        screen.getByText(/saved/i)
      ).toBeInTheDocument();
    });
  });

  it('displays error message on validation failure', async () => {
    const user = userEvent.setup();
    const mockProfile = {
      robotics_experience: 'beginner',
      programming_experience: 'beginner',
      ai_ml_experience: 'none',
      learning_goals: 'Test',
      preferred_learning_style: 'visual',
      weekly_time_commitment: 5,
    };

    jest.spyOn(api, 'get').mockResolvedValueOnce({ data: mockProfile });
    jest.spyOn(api, 'post').mockRejectedValueOnce({
      response: {
        status: 422,
        data: { detail: 'Invalid experience level' },
      },
    });

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test')).toBeInTheDocument();
    });

    const saveButton = screen.getByRole('button', { name: /save/i });
    await user.click(saveButton);

    // Should show error message
    await waitFor(() => {
      expect(screen.getByText(/invalid experience level/i)).toBeInTheDocument();
    });
  });

  it('shows loading state while fetching data', () => {
    jest.spyOn(api, 'get').mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 1000))
    );

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    // Should show loading indicator
    // Add specific check based on implementation
    expect(screen.queryByRole('button', { name: /save/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    const user = userEvent.setup();
    const mockProfile = {
      robotics_experience: 'beginner',
      programming_experience: 'beginner',
      ai_ml_experience: 'none',
      learning_goals: 'Test',
      preferred_learning_style: 'visual',
      weekly_time_commitment: 5,
    };

    jest.spyOn(api, 'get').mockResolvedValueOnce({ data: mockProfile });

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Test')).toBeInTheDocument();
    });

    // Clear required field
    const goalsInput = screen.getByLabelText(/learning goals/i);
    await user.clear(goalsInput);

    const saveButton = screen.getByRole('button', { name: /save/i });
    await user.click(saveButton);

    // Should show validation error
    await waitFor(() => {
      expect(screen.getByText(/required/i)).toBeInTheDocument();
    });
  });
});

*/

// Placeholder tests - uncomment actual tests above when Profile page is implemented
describe('Profile Page', () => {
  it.todo('loads existing profile data on mount');
  it.todo('submits profile updates successfully');
  it.todo('handles API errors during load');
  it.todo('handles API errors during submit');
  it.todo('validates required fields');
});

