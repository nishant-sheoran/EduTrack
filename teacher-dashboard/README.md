# Teacher Dashboard

A modern, responsive teacher dashboard built with Next.js, TypeScript, and Tailwind CSS. Features real-time data visualization, system health monitoring, and configuration management.

## Features

### 🎯 Core Components

- **KPIBox**: Displays key performance indicators with delta values and icons
- **ChartBox**: Interactive charts using Recharts (line and bar charts)  
- **VideoBox**: Session video player with session details and subject categorization
- **TranscriptList**: Downloadable transcript management with subject filtering
- **ConfigPanel**: Configuration settings with real-time class inputs and localStorage persistence
- **SystemHealthPanel**: Real-time system status monitoring

### 🚀 Real-Time Features

- **Live Attendance Calculation**: Uses teacher input (total students) and engagement model detection (students in frame) to calculate real-time attendance percentage
- **Live Engagement Tracking**: Analyzes detected faces for engagement scores and calculates average engagement percentage
- **Subject Categorization**: Teacher can set current subject which automatically categorizes new transcripts and video sessions
- **Auto-Refresh**: KPIs update every 5 seconds, system health every 10 seconds for real-time monitoring

### 🎨 Design System

- **Dark Mode First**: Built with dark theme as default
- **Responsive Grid**: CSS Grid with Tailwind's @layer for custom grid areas
- **Interactive Elements**: Hover effects, scale animations, and smooth transitions
- **Custom Scrollbars**: Styled scrollbars for better UX
- **Toast Notifications**: User feedback system for actions

### 🔧 Technical Features

- **TypeScript**: Full type safety throughout the application
- **Custom Hooks**: 
  - `useDashboardData`: Manages dashboard data with real-time updates
  - `useSystemHealth`: System health monitoring with auto-refresh
  - `useLocalStorage`: Type-safe localStorage persistence
- **Context Providers**: Global state management for config and toasts
- **Mock Data**: Simulated API responses for development

## Project Structure

```
src/
├── app/
│   ├── dashboard/
│   │   └── page.tsx          # Main dashboard page
│   ├── globals.css           # Global styles with @layer components
│   └── layout.tsx            # Root layout with providers
├── components/
│   ├── BentoGrid.tsx         # CSS Grid layout component
│   ├── KPIBox.tsx            # Key performance indicators
│   ├── ChartBox.tsx          # Chart visualization component
│   ├── VideoBox.tsx          # Video session player
│   ├── TranscriptList.tsx    # Transcript management
│   ├── ConfigPanel.tsx       # Configuration settings
│   ├── SystemHealthPanel.tsx # System health monitoring
│   └── Toast.tsx             # Toast notification component
├── contexts/
│   ├── ConfigContext.tsx     # Global configuration state
│   └── ToastContext.tsx      # Toast notification management
├── hooks/
│   ├── useDashboardData.ts   # Dashboard data management
│   ├── useSystemHealth.ts    # System health monitoring
│   ├── useLocalStorage.ts    # localStorage persistence
│   └── useRealTimeKPIs.ts    # Real-time engagement and attendance calculation
├── lib/
│   └── mockData.ts           # Mock API data and interfaces
└── styles/
    └── bento-grid.css        # CSS Grid area definitions
```

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Available Scripts

- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Teacher Input Configuration

### Real-Time Class Settings

The dashboard includes two critical teacher inputs that enable real-time calculations:

1. **Total Students in Class**: Used for attendance percentage calculation
   - Input: Number field (1-200 students)
   - Updates KPIs automatically when changed
   - Formula: `Attendance % = (Students Detected in Frame / Total Students) × 100`

2. **Current Subject**: Used for content categorization
   - Input: Dropdown with predefined subjects or "Other" option
   - Automatically categorizes new transcripts and video sessions
   - Enables subject-based filtering in transcript list

### How It Works

1. Teacher sets total class size and current subject in Configuration panel
2. Engagement model detects students in camera frame every 5 seconds
3. System calculates live attendance: `detected students / total students`
4. System calculates live engagement: `average engagement score from detected faces`
5. All new content (transcripts, videos) gets tagged with current subject

## Component Usage

### KPIBox
```tsx
<KPIBox 
  title="Live Attendance"
  value="92.5%"
  delta={2.1}
  icon={<Users />}
  accentColor="text-emerald-400"
/>
```

### ChartBox
```tsx
<ChartBox 
  type="line"
  data={chartData}
  title="Engagement Timeline"
  dataKey="engagement"
  accentColor="#34d399"
/>
```

### ConfigPanel
```tsx
<ConfigPanel />
// Automatically uses ConfigContext for state management
```

### SystemHealthPanel
```tsx
<SystemHealthPanel />
// Automatically uses useSystemHealth hook
```

## Styling

### Tailwind CSS with @layer

The project uses Tailwind CSS v4 with custom @layer components for:

- Interactive buttons with hover/active states
- Custom slider styling
- Custom scrollbars
- Loading animations

### CSS Grid Areas

Custom grid areas are defined in `bento-grid.css`:

```css
@layer utilities {
  .bento-grid-areas {
    grid-template-areas:
      'kpi1 kpi1 kpi2 kpi2 video video'
      'chart1 chart1 chart1 chart2 chart2 chart2'
      'transcripts transcripts config config system system'
      'transcripts transcripts config config system system';
  }
}
```

## State Management

### Context Providers

- **ConfigProvider**: Manages global configuration with localStorage persistence
- **ToastProvider**: Manages toast notifications across the application

### Custom Hooks

- **useDashboardData**: Fetches and manages dashboard data with real-time updates
- **useSystemHealth**: Monitors system health with auto-refresh
- **useLocalStorage**: Type-safe localStorage wrapper
- **useRealTimeKPIs**: Calculates live attendance and engagement based on teacher inputs and engagement model

## Data Flow

1. **Mock Data**: Simulated API responses in `/lib/mockData.ts`
2. **Hooks**: Custom hooks fetch and manage data
3. **Context**: Global state management for config and toasts
4. **Components**: UI components consume data and state
5. **User Interactions**: Actions trigger toasts and state updates

## Responsive Design

The dashboard is fully responsive with:

- Mobile-first approach
- CSS Grid areas for desktop layout
- Flexible components that adapt to screen size
- Touch-friendly interactions

## Browser Support

- Modern browsers with CSS Grid support
- ES6+ JavaScript features
- CSS Custom Properties

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
