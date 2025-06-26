
# Sen-Social: AI-Powered Social Media Content Generator

A Django web application powered by AI agents that generates engaging social media content using a reflection-based improvement loop. The application features a modern web interface for creating, managing, and sharing AI-generated social media posts.

## 🌟 Features

### AI Agent Capabilities
- **Tool-Enabled Agent**: Uses Tavily search to fetch latest news and information
- **Time-Aware**: Gets current date/time for contextual posts
- **Reflection Loop**: Automatically critiques and improves generated content
- **Customizable Topics**: Generate content for any topic or theme
- **Viral Optimization**: Optimized for engagement, brevity, and impact

### Web Application Features
- **🖥️ Modern Web Interface**: Clean, responsive Django-based UI
- **👤 User Authentication**: Secure login/logout system
- **📝 Post Management**: Create, edit, delete, and organize posts
- **📊 Post Status Tracking**: Draft, Published, and Archived states
- **🔍 Search & Filter**: Find posts by content, title, or status
- **📱 Social Media Sharing**: Direct sharing to X, Facebook, LinkedIn, Instagram
- **📥 Export Options**: Copy content or download as text files
- **📋 Conversation History**: View the AI generation and reflection process

## 🏗️ Architecture

### Project Structure

```
sen-social/
├── venv/                          # Virtual environment
├── .env                          # Environment variables & API keys
├── manage.py                     # Django management script
├── config/                       # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI application
├── agents/                       # Main Django app
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Database models (Post model)
│   ├── views.py                 # Web views and logic
│   ├── urls.py                  # App URL patterns
│   ├── agents/                  # AI agent modules
│   │   ├── __init__.py
│   │   ├── reflect_agent.py     # LangGraph-based agent
│   │   ├── chains.py            # LLM chains and prompts
│   │   └── tools.py             # Search and time tools
│   └── templates/               # HTML templates
│       └── agents/
│           ├── dashboard.html   # Main dashboard
│           ├── result.html      # Generation results
│           ├── post_list.html   # Post management
│           ├── post_detail.html # Post viewing
│           ├── post_edit.html   # Post editing
│           └── post_delete.html # Post deletion
├── templates/                    # Base templates
│   ├── base.html                # Base layout
│   └── registration/
│       └── login.html           # Login page
├── static/                       # CSS, JavaScript, images
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

### Core Components

#### AI Agent System
- **`reflect_agent.py`**: LangGraph-based implementation with visual workflow
- **`chains.py`**: LLM chains for generation and reflection
- **`tools.py`**: Search and time tools for context

#### Django Web Application
- **Models**: Post model for storing generated content and metadata
- **Views**: Web interface for agent interaction and post management
- **Templates**: Modern, responsive HTML interface
- **Authentication**: User login/logout system

## 🚀 Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd sen-social
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: LangSmith Tracing
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=sen-social

# Django Settings
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

5. **Initialize Django database**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
Open your browser and go to: `http://127.0.0.1:8000`

### Getting API Keys

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Generate a new API key

#### Tavily API Key
1. Visit [Tavily](https://tavily.com/)
2. Sign up for an account
3. Get your API key from the dashboard

## 🎯 Usage

### Web Application

1. **Start the Django server**
```bash
python manage.py runserver
```

2. **Access the dashboard**
Navigate to `http://127.0.0.1:8000` in your browser

3. **Generate content**
   - Enter your content prompt in the dashboard
   - Click "Generate Content" to start the AI agent
   - Watch the real-time generation and reflection process
   - Save the result as a draft when satisfied

4. **Manage posts**
   - View all your posts in the post list
   - Edit existing drafts
   - Change post status (Draft → Published → Archived)
   - Search and filter posts by status or content

5. **Share content**
   - Use the social media buttons to share directly to platforms
   - **X (Twitter)**: Opens native share dialog with character limits
   - **Facebook**: Share via Facebook's share dialog
   - **LinkedIn**: Professional sharing format
   - **Instagram**: Copy content to clipboard for manual posting

### Features Walkthrough

#### Content Generation Process
1. **Input**: Enter your topic or content request
2. **Search**: AI agent searches for current, relevant information
3. **Generate**: Creates initial social media post
4. **Reflect**: AI critiques the post for improvements
5. **Improve**: Generates refined version based on feedback
6. **Iterate**: Repeats reflection and improvement for better results
7. **Save**: Store the final result as a managed post

#### Post Management
- **Create**: Generate new content using AI agent
- **Read**: View post details and generation history
- **Update**: Edit title, content, and status
- **Delete**: Remove posts permanently
- **Search**: Find posts by title, content, or original prompt
- **Filter**: View posts by status (Draft, Published, Archived)

### Command Line Usage (Advanced)

For direct agent interaction without the web interface:

```python
# In Python shell or script
from agents.agents.reflect_agent import process_user_request

# Generate content
result = process_user_request(
    "Latest developments in renewable energy technology"
)

print("Final Post:", result['final_post'])
print("Generation Steps:", len(result['conversation_history']))
```

## 🔧 Configuration

### Django Settings

Key configuration options in `config/settings.py`:

- **Database**: Currently uses SQLite for development
- **Authentication**: Login/logout URLs and redirect settings
- **Templates**: Django template system (Jinja2 migration planned)
- **Static Files**: CSS, JavaScript, and image handling

### AI Agent Configuration

#### Prompt Customization
Edit `agents/agents/chains.py` to modify:
- `GENERATION_PROMPT_FIRST`: Initial generation instructions
- `GENERATION_PROMPT_ADJUSTMENTS`: Refinement instructions
- `reflection_prompt`: Critique criteria and feedback style

#### Tool Configuration
In `agents/agents/tools.py`:
- **Search Settings**: Modify `search_depth="basic"` for Tavily search
- **Time Format**: Adjust `get_system_time(format="%Y-%m-%d %H:%M:%S")`

#### Agent Behavior
In `agents/agents/reflect_agent.py`:
- **Iteration Limit**: Change `len(state) > 6` to adjust reflection cycles
- **Stopping Criteria**: Modify the `should_continue` function

### Environment Variables

Additional optional settings for `.env`:

```env
# Django Debug Mode
DEBUG=True

# Database URL (for production)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Allowed Hosts (for production)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

## 🧠 How It Works

### AI Agent Workflow

The application uses a sophisticated LangGraph-based agent system:

1. **🔍 Research Phase**: 
   - Agent receives user's content request
   - Uses Tavily search API to gather current, relevant information
   - Incorporates real-time data and trending topics

2. **✨ Generation Phase**: 
   - Creates initial social media post using GPT-4
   - Optimizes for engagement, brevity, and viral potential
   - Includes relevant hashtags and compelling hooks

3. **🧠 Reflection Phase**: 
   - AI critiques its own output for improvements
   - Evaluates clarity, engagement, factual accuracy
   - Identifies areas for enhancement

4. **🔄 Improvement Phase**: 
   - Generates refined version based on self-critique
   - Iterates up to 3 times for optimal results
   - Balances creativity with factual accuracy

5. **💾 Persistence Phase**:
   - Saves final result to Django database
   - Stores full conversation history for transparency
   - Enables future editing and management

### Database Schema

#### Post Model
```python
class Post(models.Model):
    title = CharField(max_length=200)              # Brief post title
    content = TextField()                          # Generated content
    original_prompt = TextField()                  # User's original request
    status = CharField(choices=STATUS_CHOICES)     # Draft/Published/Archived
    created_by = ForeignKey(User)                  # Post owner
    created_at = DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = DateTimeField(auto_now=True)      # Last modification
    conversation_history = JSONField()             # Generation process
    generation_metadata = JSONField()             # Additional metadata
```

### Social Media Integration

#### Platform-Specific Optimizations
- **X (Twitter)**: 280 character limit handling, trending hashtags
- **Facebook**: Engaging hooks and shareable formats
- **LinkedIn**: Professional tone and industry insights
- **Instagram**: Visual descriptions and relevant hashtags

#### Sharing Mechanism
- **Direct URL Sharing**: Uses native platform share APIs
- **Content Optimization**: Platform-specific character limits
- **Clipboard Integration**: For platforms without direct sharing
- **Mobile Responsive**: Optimized share dialogs for all devices

## 📊 Example Workflow

### Web Application Flow
```
🌐 User visits dashboard
📝 Enters content prompt: "Latest AI breakthroughs in healthcare"
🤖 AI agent starts processing...

--- Generation Process ---
🔍 Searching for current AI healthcare news...
✨ Generating initial post...
🧠 Reflecting on content quality...
� Improving based on feedback...
✅ Final optimized post ready!

--- Result Management ---
💾 Save as draft post
� Edit title and content if needed
📊 Change status to "Published"
🚀 Share directly to social platforms
```

### Sample AI-Generated Content

**Input Prompt**: "Latest developments in renewable energy storage technology"

**AI Agent Process**:
1. **Research**: Finds recent news about battery technology breakthroughs
2. **Generation**: Creates engaging post with current data
3. **Reflection**: "Could be more specific about the impact on consumers"
4. **Improvement**: Adds concrete benefits and cost implications

**Final Output**:
```
� BREAKTHROUGH: New solid-state batteries charge 10x faster than lithium-ion! 

Tesla's latest tech could cut EV charging time to under 6 minutes by 2025. 

This changes everything for electric adoption. 

#CleanEnergy #EVs #Innovation #Tesla #Sustainability
```

### Dashboard Features

#### Content Generation
- **Real-time progress indicators** during AI processing
- **Step-by-step visibility** into generation and reflection
- **Conversation history preservation** for transparency
- **Save draft functionality** with custom titles

#### Post Management
- **List view** with search and filtering
- **Detailed post view** with full conversation history
- **Inline editing** with live preview
- **Status management** (Draft → Published → Archived)
- **Bulk operations** for post organization

#### Social Sharing
- **One-click sharing** to major platforms
- **Platform-optimized content** with proper formatting
- **Character limit handling** for Twitter/X
- **Copy-to-clipboard** for Instagram and manual posting

## 🛠️ Technologies

### Backend Stack
- **Django 5.x**: Web framework and ORM
- **Python 3.8+**: Core programming language
- **SQLite**: Development database (PostgreSQL for production)
- **LangChain**: LLM framework and prompt management
- **LangGraph**: Agent workflow orchestration
- **OpenAI GPT-4**: Core language model for generation and reflection

### AI & Integration
- **Tavily API**: Real-time web search and information retrieval
- **LangSmith**: Optional agent monitoring and debugging
- **JSON**: Conversation history and metadata storage

### Frontend & UI
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icons and visual elements
- **Vanilla JavaScript**: Interactive features and AJAX
- **Django Templates**: Server-side rendering (Jinja2 migration planned)

### Development Tools
- **python-decouple**: Environment variable management
- **Django Admin**: Built-in administration interface
- **Git**: Version control and collaboration

### Social Media APIs
- **Native Share URLs**: No API keys required for sharing
- **Platform-specific optimization**: Character limits and formatting
- **Clipboard API**: For platforms without direct sharing support

## � Roadmap

### Current Phase (Completed)
- ✅ Django web application with authentication
- ✅ AI agent integration with LangGraph
- ✅ Post management (CRUD operations)
- ✅ Social media sharing buttons
- ✅ Responsive web design

### Phase 2: Template Engine Upgrade
- [ ] Migrate to Jinja2 templating for better syntax
- [ ] Improved template logic and conditionals
- [ ] Enhanced developer experience

### Phase 3: Advanced Features
- [ ] Real-time WebSocket updates during generation
- [ ] API endpoints for external integrations
- [ ] Performance optimization and caching
- [ ] Advanced search and filtering

### Phase 4: Production Ready
- [ ] PostgreSQL database migration
- [ ] Security hardening and testing
- [ ] Comprehensive documentation
- [ ] CI/CD pipeline setup

### Phase 5: Containerization
- [ ] Docker and Docker Compose setup
- [ ] Production deployment configuration
- [ ] Scalability improvements
- [ ] Monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain Community**: For the excellent LLM framework
- **OpenAI**: For GPT-4 language model
- **Tavily**: For real-time search capabilities
- **Django Community**: For the robust web framework
- **Bootstrap Team**: For the responsive UI framework