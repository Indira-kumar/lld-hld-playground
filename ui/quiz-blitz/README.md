# QuizBlitz
The pitch: A trivia quiz app where you race against a per-question timer, build streaks, and lose lives if you're wrong or too slow. Think Kahoot meets Duolingo - snappy, satisfying, and stateful.

# Goal
Use [RADIO framework](https://www.greatfrontend.com/front-end-system-design-playbook/framework) to understand the requirement and code the same

# Requirement
## Functional Requirements:
- User selects a category (Science, History, Sports) and difficulty (Easy/Medium/Hard)
- Game consists of 10 questions, shown one at a time
- Each question has 4 multiple choice options and a 15s countdown timer
- Correct answer → award points (base + streak bonus)
- Wrong answer OR timeout → lose a life, break streak
- Player starts with 3 lives; losing all ends the game early
- Streak = consecutive correct answers; tracked throughout session
- Results screen shows: total score, accuracy %, longest streak

## Non-Functional Requirements (performance, UX, constraints)
- Timer must be visually smooth and accurate (no drift)
- Question transitions should be animated
- All 10 questions prefetched at session start - no mid-game loading
- Mobile-first responsive layout
- Perceived load time < 1s on session start

## Out of Scope
- no offline tolerance
- no auth, or leaderboard
- no multiplayer mode

# Architecture
## Screens needed
- Home Screen (difficulty and topics are choosen here)
- Quiz screen (each question is shown one at a time)
- Results screen

## Components needed
- Base Container
- Multiple Choice buttons (for difficulty and topic)
- Question
- Answer (4 radio buttons with labels)
- result metric
- Counter
- Timer
- Progress bar

## Layers
- View layer (the UI users see)
- Store layer (the state of the app)
- Data access Layer (the API layer)
- server (TRIVIA api - black box to UI)

## Architecture
https://excalidraw.com/#json=tD3jDMcnQ16oDMbgSpnuo,XfAiofrv5QNMryuiURdGsA

# Data Model
## API response
```
{
  "response_code": 0,
  "results": [
    {
      "type": "multiple",
      "difficulty": "medium",
      "category": "Science &amp; Nature",
      "question": "What is the lowest layer of the Earth&#039;s atmosphere named?",
      "correct_answer": "Troposphere",
      "incorrect_answers": [
        "Stratosphere",
        "Mesosphere",
        "Thermosphere"
      ]
    },
...
  ]
}
```

## Store Shape
DAL Layer could be used for the following 3 responsibilities:
- Cleaning the response (decoding HTML entities)
- shuffle the answer in the options
- Generate stable ID per question
```
type RawQuestion = {
  type: string,
  difficulty: 'easy' | 'medium' | 'hard';
  category: string;
  question: string;           // HTML encoded
  correct_answer: string;
  incorrect_answers: string[];
}

type Question = {
  id: string,                 // generated: `q_${index}`
  type: string,
  question: string;           // decoded HTML
  options: string[];          // shuffled [correct + 3 incorrect]
  correctAnswer: string;
  category: string;
  difficulty: 'easy' | 'medium' | 'hard';
}
```

Tanstack/react query to store API data, this is the hook used:
```
const useQuestions = (category: string, difficulty: string) => {
  return useQuery({
    queryKey: ['questions',category, difficulty, sessionId],
    queryFn: () => fetchAndTransform(category, difficulty),
    staleTime: Infinity, // so no refetch
    gcTime: 5 * 60 * 1000 // 5 mins TTL
  })
}
```

Zustand to store game state. This is the shape:
```
type GamePhase = 
  | 'start'        // home screen, nothing selected
  | 'loading'     // fetching questions
  | 'playing'     // active question
  | 'finished'    // all 10 questions done or time out

type AnswerRecord = {
  questionId: string;
  selectedAnswer: string | null;  // null = timeout
  isCorrect: boolean;
  timeTaken: number;              // ms — useful for score calculation 
}

type GameState = {
  // Config (set on home screen)
  category: string | null;
  difficulty: 'easy' | 'medium' | 'hard' | null;

  // Session state
  phase: GamePhase;
  currentQuestionIndex: number;   // 0–9
  lives: number;                  // starts at 3
  score: number;
  streak: number;                 // resets on wrong/timeout
  longestStreak: number;          // never resets, but gets updated each time streak is lost or at game end
  answers: AnswerRecord[];        // full history → used for results screen

  // Actions
  startGame: (category: string, difficulty: string) => void;
  submitAnswer: (answer: string | null) => void;  // null = timeout
  nextQuestion: () => void;
  resetGame: () => void;
```

# Interface
Interface for few of the dumb components:

```
<QuestionCard question="What is the capital of France?" questionNumber={3} />

<AnswerOption 
  label="Paris"
  onSelect={(answer) => { /* parent decides what to do */ }}
/>
```

Smart Screen components consisting of dumb components:
1) Quiz screen
```
QuizScreen (SMART — owns store connection)
  ├── reads currentQuestion from React Query
  ├── reads lives, streak, score from Zustand
  ├── calls submitAnswer(), nextQuestion() from Zustand
  │
  ├── <QuestionCard question={...} questionNumber={...} />   ← DUMB
  ├── <AnswerOption label={...} onSelect={...} />            ← DUMB  
  ├── <Timer duration={15} onTimeout={...} />                ← DUMB
  ├── <LivesIndicator lives={3} />                           ← DUMB
  └── <StreakCounter streak={5} />                           ← DUMB
```

# Optimization
- Prefetch or eager fetch all the questions
- Use transitions to feel question to question switch smoother and feel faster
- If trivia API is slow, use a loader, and keep the user informed of the slowness, have a timeout and resort to a default set of questions for each category and difficulty.
- Timer ticks every second. If Timer lives inside QuizScreen, it re-renders QuizScreen + all 4 AnswerOptions every second. That's wasteful. So isolate timer

# Code Reference
1. Zustand store (game state + actions)
2. DAL: useQuestions hook (React Query + transformer)
3. HomeScreen (category/difficulty picker + prefetch trigger)
4. QuizScreen (smart container - wires everything)
5. QuestionCard, AnswerOption, Timer, LivesIndicator (dumb components)
6. ResultsScreen (reads from store)
7. Animations (Framer Motion last)