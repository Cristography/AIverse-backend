# Complete API Documentation for React Frontend

## Table of Contents

1. [Authentication & User Management](#authentication--user-management)
2. [Prompts API](#prompts-api)
3. [Content API (Blogs, News, Tools)](#content-api)
4. [Interactions API (Comments, Votes, Bookmarks)](#interactions-api)
5. [Tags API](#tags-api)
6. [Permission System](#permission-system)
7. [Placeholder System for Prompts](#placeholder-system-for-prompts)
8. [Multi-language Support](#multi-language-support)
9. [Error Responses](#error-responses)

---

## Authentication & User Management

### Base URL

```
http://localhost:8000/api/auth/
```

### 1. Register New User

**Endpoint:** `POST /auth/register/`  
**Permission:** Public  
**Request Body:**

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Success Response (201):**

```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "is_pro": false,
  "is_moderator": false,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

### 2. Login

**Endpoint:** `POST /auth/login/`  
**Permission:** Public  
**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "",
    "role": "user",
    "full_name": "John Doe",
    "is_pro": false,
    "is_moderator": false,
    "date_joined": "2024-01-15T10:30:00Z"
  }
}
```

### 3. Refresh Token

**Endpoint:** `POST /auth/token/refresh/`  
**Permission:** Public  
**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response (200):**

```json
{
  "access": "new-access-token-here",
  "refresh": "new-refresh-token-here"
}
```

### 4. Get Current User

**Endpoint:** `GET /auth/me/`  
**Permission:** Authenticated  
**Headers:** `Authorization: Bearer {access_token}`  
**Success Response (200):**

```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Full stack developer",
  "role": "user",
  "full_name": "John Doe",
  "is_pro": false,
  "is_moderator": false,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

### 5. Update Current User Profile

**Endpoint:** `PATCH /auth/me/`  
**Permission:** Authenticated  
**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "bio": "Senior developer and AI enthusiast"
}
```

**Success Response (200):** Same as Get Current User

### 6. Get User by Username

**Endpoint:** `GET /auth/users/{username}/`  
**Permission:** Public  
**Success Response (200):** Same as Get Current User

---

## Prompts API

### Base URL

```
http://localhost:8000/api/prompts/
```

### 1. List All Prompts

**Endpoint:** `GET /prompts/`  
**Permission:** Public  
**Query Parameters:**

- `type` (text, image, music)
- `author__username` (filter by author)
- `search` (search in title and body)
- `ordering` (-created_at, created_at, -views, views, title)
- `page` (pagination)
- `page_size` (default: 20)

**Example Request:**

```
GET /prompts/?type=text&ordering=-created_at&page=1
```

**Success Response (200):**

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/prompts/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "type": "text",
      "title": "Professional Email Writer",
      "slug": "professional-email-writer",
      "body": "Write a professional email about {TOPIC} with a {TONE} tone, addressing {RECIPIENT}. Include {KEY_POINTS} in the message.",
      "context": {
        "model": "gpt-4",
        "temperature": 0.7
      },
      "author": {
        "id": "uuid",
        "username": "johndoe",
        "full_name": "John Doe"
      },
      "views": 1250,
      "vote_count": 45,
      "tags": ["email", "professional", "writing"],
      "is_bookmarked": false,
      "user_vote": null,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-16T14:20:00Z"
    }
  ]
}
```

### 2. Get Single Prompt

**Endpoint:** `GET /prompts/{slug}/`  
**Permission:** Public  
**Success Response (200):** Same as single prompt object above (also increments view count)

### 3. Create Prompt

**Endpoint:** `POST /prompts/`  
**Permission:** Authenticated  
**Request Body:**

```json
{
  "type": "text",
  "title": "Blog Post Generator",
  "body": "Write a {LENGTH} blog post about {TOPIC} in a {STYLE} style. Target audience: {AUDIENCE}. Include these points: {KEY_POINTS}",
  "context": {
    "model": "gpt-4",
    "temperature": 0.8
  },
  "tags": ["blog", "content", "writing"]
}
```

**Success Response (201):** Same as Get Single Prompt

### 4. Update Prompt

**Endpoint:** `PATCH /prompts/{slug}/`  
**Permission:** Owner or Moderator  
**Request Body:** Same as Create (partial updates allowed)  
**Success Response (200):** Updated prompt object

### 5. Delete Prompt

**Endpoint:** `DELETE /prompts/{slug}/`  
**Permission:** Owner or Moderator  
**Success Response (204):** No content

### 6. Get My Prompts

**Endpoint:** `GET /prompts/my_prompts/`  
**Permission:** Authenticated  
**Success Response (200):** Paginated list of user's prompts

### 7. Get Prompt Relations

**Endpoint:** `GET /prompts/{slug}/relations/`  
**Permission:** Public  
**Success Response (200):**

```json
[
  {
    "source_prompt": { /* prompt object */ },
    "target_prompt": { /* prompt object */ },
    "relation_type": "improved_version",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## Content API

### Blogs

**Base URL:** `http://localhost:8000/api/blogs/`

#### 1. List All Blogs

**Endpoint:** `GET /blogs/`  
**Permission:** Public  
**Query Parameters:** `search`, `ordering`, `page`  
**Success Response (200):**

```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "title": "Getting Started with AI Prompts",
      "slug": "getting-started-with-ai-prompts",
      "content": "Full blog content here...",
      "author": {
        "id": "uuid",
        "username": "moderator1",
        "full_name": "Jane Smith"
      },
      "tags": ["tutorial", "ai", "beginners"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. Get Single Blog

**Endpoint:** `GET /blogs/{slug}/`  
**Permission:** Public  
**Success Response (200):** Single blog object

#### 3. Create Blog

**Endpoint:** `POST /blogs/`  
**Permission:** Moderator or Admin  
**Request Body:**

```json
{
  "title": "Advanced Prompt Engineering",
  "content": "Detailed blog content...",
  "tags": ["advanced", "prompts", "techniques"]
}
```

**Success Response (201):** Created blog object

#### 4. Update Blog

**Endpoint:** `PATCH /blogs/{slug}/`  
**Permission:** Owner or Moderator  
**Success Response (200):** Updated blog object

#### 5. Delete Blog

**Endpoint:** `DELETE /blogs/{slug}/`  
**Permission:** Owner or Moderator  
**Success Response (204):** No content

### News

**Base URL:** `http://localhost:8000/api/news/`

All endpoints identical to Blogs, same structure:

- `GET /news/` - List all
- `GET /news/{slug}/` - Get single
- `POST /news/` - Create (Moderator+)
- `PATCH /news/{slug}/` - Update (Owner/Moderator)
- `DELETE /news/{slug}/` - Delete (Owner/Moderator)

**Response Structure:**

```json
{
  "id": "uuid-here",
  "title": "New AI Model Released",
  "slug": "new-ai-model-released",
  "content": "News content here...",
  "author": { /* author object */ },
  "tags": ["news", "ai", "release"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Tools

**Base URL:** `http://localhost:8000/api/tools/`

#### 1. List All Tools

**Endpoint:** `GET /tools/`  
**Permission:** Public  
**Query Parameters:** `type` (filter by tool type), `search`, `ordering`  
**Success Response (200):**

```json
{
  "count": 75,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "name": "ChatGPT",
      "slug": "chatgpt",
      "description": "Advanced language model by OpenAI",
      "url": "https://chat.openai.com",
      "type": {
        "id": "uuid",
        "name": "Text Generation",
        "description": "AI tools for generating text"
      },
      "author": {
        "id": "uuid",
        "username": "moderator1",
        "full_name": "Jane Smith"
      },
      "tags": ["ai", "chatbot", "text-generation"],
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. Get Single Tool

**Endpoint:** `GET /tools/{slug}/`  
**Permission:** Public

#### 3. Create Tool

**Endpoint:** `POST /tools/`  
**Permission:** Moderator or Admin  
**Request Body:**

```json
{
  "name": "DALL-E 3",
  "description": "AI image generation tool",
  "url": "https://openai.com/dall-e-3",
  "type_id": "uuid-of-tool-type",
  "tags": ["image", "ai", "generation"]
}
```

#### 4. Update Tool

**Endpoint:** `PATCH /tools/{slug}/`  
**Permission:** Owner or Moderator

#### 5. Delete Tool

**Endpoint:** `DELETE /tools/{slug}/`  
**Permission:** Owner or Moderator

### Tool Types

**Base URL:** `http://localhost:8000/api/tool-types/`

#### 1. List All Tool Types

**Endpoint:** `GET /tool-types/`  
**Permission:** Public  
**Success Response (200):**

```json
[
  {
    "id": "uuid-here",
    "name": "Text Generation",
    "description": "Tools for generating text content"
  },
  {
    "id": "uuid-here",
    "name": "Image Generation",
    "description": "Tools for creating images"
  }
]
```

#### 2. Create Tool Type

**Endpoint:** `POST /tool-types/`  
**Permission:** Moderator or Admin  
**Request Body:**

```json
{
  "name": "Audio Generation",
  "description": "Tools for creating audio and music"
}
```

---

## Interactions API

### Comments

**Base URL:** `http://localhost:8000/api/comments/`

#### 1. List Comments

**Endpoint:** `GET /comments/`  
**Permission:** Public  
**Query Parameters:**

- `commentable_type` (1=prompts, 2=tools, 3=news, 4=blogs)
- `commentable_id` (UUID of the item)

**Example Request:**

```
GET /comments/?commentable_type=1&commentable_id=uuid-of-prompt
```

**Success Response (200):**

```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "commentable_type": 1,
      "commentable_id": "uuid-of-prompt",
      "author": {
        "id": "uuid",
        "username": "johndoe",
        "full_name": "John Doe"
      },
      "body": "Great prompt! Works perfectly for my use case.",
      "is_edited": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 2. Create Comment

**Endpoint:** `POST /comments/`  
**Permission:** Authenticated  
**Request Body:**

```json
{
  "commentable_type": 1,
  "commentable_id": "uuid-of-prompt",
  "body": "This is really helpful, thank you!"
}
```

**Success Response (201):** Created comment object

#### 3. Update Comment

**Endpoint:** `PATCH /comments/{id}/`  
**Permission:** Owner only  
**Request Body:**

```json
{
  "body": "Updated comment text"
}
```

**Success Response (200):** Updated comment (is_edited=true)

#### 4. Delete Comment

**Endpoint:** `DELETE /comments/{id}/`  
**Permission:** Owner or Moderator  
**Success Response (204):** No content

### Votes

**Base URL:** `http://localhost:8000/api/votes/`

#### 1. Get My Votes

**Endpoint:** `GET /votes/`  
**Permission:** Authenticated  
**Success Response (200):**

```json
[
  {
    "votable_type": 1,
    "votable_id": "uuid-of-prompt",
    "value": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### 2. Vote or Update Vote

**Endpoint:** `POST /votes/`  
**Permission:** Authenticated  
**Request Body:**

```json
{
  "votable_type": 1,
  "votable_id": "uuid-of-prompt",
  "value": 1
}
```

**Note:** `value` must be `1` (upvote) or `-1` (downvote)  
**Success Response (201 if new, 200 if updated):** Vote object

#### 3. Remove Vote

**Endpoint:** `DELETE /votes/remove_vote/`  
**Permission:** Authenticated  
**Query Parameters:**

- `votable_type` (required)
- `votable_id` (required)

**Example Request:**

```
DELETE /votes/remove_vote/?votable_type=1&votable_id=uuid-of-prompt
```

**Success Response (204):** No content

### Bookmarks

**Base URL:** `http://localhost:8000/api/bookmarks/`

#### 1. Get My Bookmarks

**Endpoint:** `GET /bookmarks/`  
**Permission:** Authenticated  
**Success Response (200):**

```json
[
  {
    "bookmarkable_type": 1,
    "bookmarkable_id": "uuid-of-prompt",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

#### 2. Add Bookmark

**Endpoint:** `POST /bookmarks/`  
**Permission:** Authenticated  
**Request Body:**

```json
{
  "bookmarkable_type": 1,
  "bookmarkable_id": "uuid-of-prompt"
}
```

**Success Response (201 if new, 200 if exists):** Bookmark object

#### 3. Remove Bookmark

**Endpoint:** `DELETE /bookmarks/remove_bookmark/`  
**Permission:** Authenticated  
**Query Parameters:**

- `bookmarkable_type` (required)
- `bookmarkable_id` (required)

**Example Request:**

```
DELETE /bookmarks/remove_bookmark/?bookmarkable_type=1&bookmarkable_id=uuid-of-prompt
```

**Success Response (204):** No content

---

## Tags API

**Base URL:** `http://localhost:8000/api/tags/`

### 1. List All Tags

**Endpoint:** `GET /tags/`  
**Permission:** Public  
**Query Parameters:** `search`, `ordering`  
**Success Response (200):**

```json
[
  {
    "id": "uuid-here",
    "name": "writing",
    "usage_count": 150,
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": "uuid-here",
    "name": "ai",
    "usage_count": 320,
    "created_at": "2024-01-14T10:30:00Z"
  }
]
```

### 2. Get Tag Details

**Endpoint:** `GET /tags/{id}/`  
**Permission:** Public  
**Success Response (200):** Single tag object

### 3. Create Tag

**Endpoint:** `POST /tags/`  
**Permission:** Moderator or Admin  
**Request Body:**

```json
{
  "name": "productivity"
}
```

**Success Response (201):** Created tag object

### 4. Get Items by Tag

**Endpoint:** `GET /tags/{id}/items/`  
**Permission:** Public  
**Success Response (200):**

```json
[
  {
    "tag": "uuid-of-tag",
    "tag_name": "writing",
    "taggable_type": 1,
    "taggable_id": "uuid-of-prompt",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

## Permission System

### User Roles

| Role              | Code                                        | Capabilities                                         |
| ----------------- | ------------------------------------------- | ---------------------------------------------------- |
| **Anonymous**     | `role: null`                                | View only                                            |
| **Authenticated** | `role: "user"`                              | CRUD own prompts, vote, comment, bookmark            |
| **Pro User**      | `role: "pro"` or `is_pro: true`             | Authenticated + premium features                     |
| **Moderator**     | `role: "moderator"` or `is_moderator: true` | Pro + Create blogs/news/tools/tags, moderate content |
| **Admin**         | `role: "admin"` or `is_superuser: true`     | Full access                                          |

### Permission Matrix

| Resource       | View | Create | Edit Own | Edit Others | Delete Own | Delete Others |
| -------------- | ---- | ------ | -------- | ----------- | ---------- | ------------- |
| **Prompts**    | All  | Auth+  | Auth+    | Mod+        | Auth+      | Mod+          |
| **Blogs**      | All  | Mod+   | Mod+     | Mod+        | Mod+       | Mod+          |
| **News**       | All  | Mod+   | Mod+     | Mod+        | Mod+       | Mod+          |
| **Tools**      | All  | Mod+   | Mod+     | Mod+        | Mod+       | Mod+          |
| **Tool Types** | All  | Mod+   | Mod+     | Mod+        | Mod+       | Mod+          |
| **Tags**       | All  | Mod+   | Mod+     | Mod+        | Mod+       | Mod+          |
| **Comments**   | All  | Auth+  | Auth+    | No          | Auth+      | Mod+          |
| **Votes**      | Own  | Auth+  | Auth+    | No          | Auth+      | No            |
| **Bookmarks**  | Own  | Auth+  | N/A      | No          | Auth+      | No            |

**Note:** Moderators CANNOT edit/delete other moderators' or admins' content.

### Checking Permissions in Frontend

```javascript
// From user object returned by /auth/me/
const user = {
  role: "user",
  is_pro: false,
  is_moderator: false,
  is_superuser: false
};

// Permission checks
const canCreatePrompts = !!user; // Any authenticated user
const canCreateBlogs = user.is_moderator || user.is_superuser;
const canEditPrompt = (prompt) => 
  user.id === prompt.author.id || user.is_moderator || user.is_superuser;
const isPro = user.is_pro || user.is_moderator || user.is_superuser;
```

---

## Placeholder System for Prompts

### Syntax

Placeholders in prompt body use `{PLACEHOLDER_NAME}` format.

### Example Prompt

```json
{
  "title": "Email Writer",
  "body": "Write a {LENGTH} email about {TOPIC} with a {TONE} tone. Address it to {RECIPIENT} and include these points: {KEY_POINTS}",
  "type": "text"
}
```

### Frontend Implementation

#### 1. Parse Placeholders

```javascript
function extractPlaceholders(promptBody) {
  const regex = /\{([A-Z_]+)\}/g;
  const placeholders = [];
  let match;

  while ((match = regex.exec(promptBody)) !== null) {
    if (!placeholders.includes(match[1])) {
      placeholders.push(match[1]);
    }
  }

  return placeholders;
}

// Usage
const body = "Write a {LENGTH} email about {TOPIC}";
const placeholders = extractPlaceholders(body);
// Returns: ["LENGTH", "TOPIC"]
```

#### 2. Render Inline Form Inputs

```jsx
import React, { useState, useMemo } from 'react';

function PromptRenderer({ prompt }) {
  const [values, setValues] = useState({});

  // Extract placeholders
  const placeholders = useMemo(() => {
    return extractPlaceholders(prompt.body);
  }, [prompt.body]);

  // Initialize values
  React.useEffect(() => {
    const initialValues = {};
    placeholders.forEach(ph => {
      initialValues[ph] = '';
    });
    setValues(initialValues);
  }, [placeholders]);

  // Render prompt with inline inputs
  const renderPromptWithInputs = () => {
    let result = prompt.body;

    placeholders.forEach(placeholder => {
      const input = (
        <input
          key={placeholder}
          type="text"
          value={values[placeholder] || ''}
          onChange={(e) => setValues({
            ...values,
            [placeholder]: e.target.value
          })}
          placeholder={placeholder.toLowerCase().replace('_', ' ')}
          className="inline-input"
        />
      );

      result = result.replace(
        `{${placeholder}}`,
        `{{INPUT:${placeholder}}}`
      );
    });

    // Split and render
    const parts = result.split(/\{\{INPUT:([A-Z_]+)\}\}/);

    return parts.map((part, idx) => {
      if (placeholders.includes(part)) {
        return (
          <input
            key={idx}
            type="text"
            value={values[part] || ''}
            onChange={(e) => setValues({
              ...values,
              [part]: e.target.value
            })}
            placeholder={part.toLowerCase().replace('_', ' ')}
            className="inline-input border-b-2 border-blue-500 px-2 py-1 mx-1 focus:outline-none focus:border-blue-700"
            style={{ minWidth: '100px', display: 'inline-block' }}
          />
        );
      }
      return <span key={idx}>{part}</span>;
    });
  };

  // Generate final prompt
  const generateFinalPrompt = () => {
    let final = prompt.body;
    Object.keys(values).forEach(key => {
      final = final.replace(`{${key}}`, values[key] || `{${key}}`);
    });
    return final;
  };

  return (
    <div className="prompt-renderer">
      <h3>{prompt.title}</h3>
      <div className="prompt-body">
        {renderPromptWithInputs()}
      </div>
      <button onClick={() => {
        const final = generateFinalPrompt();
        navigator.clipboard.writeText(final);
        alert('Copied to clipboard!');
      }}>
        Copy Final Prompt
      </button>
    </div>
  );
}
```

#### 3. Alternative: Form-based Approach

```jsx
function PromptForm({ prompt }) {
  const [values, setValues] = useState({});
  const placeholders = extractPlaceholders(prompt.body);

  const handleSubmit = (e) => {
    e.preventDefault();
    let final = prompt.body;
    Object.keys(values).forEach(key => {
      final = final.replace(`{${key}}`, values[key]);
    });
    console.log('Final prompt:', final);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>{prompt.title}</h3>
      <p className="prompt-preview">{prompt.body}</p>

      <div className="placeholder-inputs">
        {placeholders.map(placeholder => (
          <div key={placeholder} className="input-group">
            <label>{placeholder.toLowerCase().replace('_', ' ')}</label>
            <input
              type="text"
              value={values[placeholder] || ''}
              onChange={(e) => setValues({
                ...values,
                [placeholder]: e.target.value
              })}
              placeholder={`Enter ${placeholder.toLowerCase()}`}
              required
            />
          </div>
        ))}
      </div>

      <button type="submit">Generate Prompt</button>
    </form>
  );
}
```

### Placeholder Guidelines for Content Creators

**Common Placeholders:**

- `{TOPIC}` - Main subject
- `{TONE}` - Writing style (formal, casual, friendly)
- `{LENGTH}` - Content length (short, medium, long)
- `{AUDIENCE}` - Target audience
- `{FORMAT}` - Output format
- `{STYLE}` - Visual/writing style
- `{LANGUAGE}` - Output language
- `{KEYWORDS}` - Important keywords
- `{RECIPIENT}` - Person being addressed
- `{KEY_POINTS}` - Main points to cover

---

## Multi-language Support (i18n)

### Language Codes

- `en` - English
- `ar` - Arabic (العربية)

### Implementation Strategy

#### 1. Backend: Add Language Field

```python
# In each model that needs translation
class Prompt(models.Model):
    # ... existing fields ...
    language = models.CharField(
        max_length=2,
        choices=[('en', 'English'), ('ar', 'Arabic')],
        default='en'
    )
```

#### 2. Frontend: React i18n Setup

```bash
npm install i18next react-i18next i18next-browser-languagedetector
```

#### 3. Translation Files

**`src/locales/en/translation.json`**

```json
{
  "nav": {
    "home": "Home",
    "prompts": "Prompts",
    "blogs": "Blogs",
    "news": "News",
    "tools": "Tools",
    "login": "Login",
    "register": "Register",
    "logout": "Logout",
    "profile": "Profile"
  },
  "prompts": {
    "title": "Prompts",
    "create": "Create Prompt",
    "search": "Search prompts...",
    "type": "Type",
    "author": "Author",
    "views": "Views",
    "votes": "Votes",
    "upvote": "Upvote",
    "downvote": "Downvote",
    "bookmark": "Bookmark",
    "comment": "Comment",
    "share": "Share",
    "edit": "Edit",
    "delete": "Delete",
    "copyPrompt": "Copy Prompt",
    "fillPlaceholders": "Fill in the placeholders below"
  },
  "forms": {
    "email": "Email",
    "username": "Username",
    "password": "Password",
    "confirmPassword": "Confirm Password",
    "firstName": "First Name",
    "lastName": "Last Name",
    "bio": "Bio",
    "submit": "Submit",
    "cancel": "Cancel",
    "save": "Save",
    "required": "This field is required"
  },
  "auth": {
    "login": "Login",
    "register": "Create Account",
    "welcomeBack": "Welcome back!",
    "newUser": "New user?",
    "existingUser": "Already have an account?",
    "signInHere": "Sign in here",
    "signUpHere": "Sign up here"
  },
  "theme": {
    "light": "Light",
    "dark": "Dark",
    "toggle": "Toggle theme"
  }
}
```

**`src/locales/ar/translation.json`**

```json
{
  "nav": {
    "home": "الرئيسية",
    "prompts": "المطالبات",
    "blogs": "المدونات",
    "news": "الأخبار",
    "tools": "الأدوات",
    "login": "تسجيل الدخول",
    "register": "إنشاء حساب",
    "logout": "تسجيل الخروج",
    "profile": "الملف الشخصي"
  },
  "prompts": {
    "title": "المطالبات",
    "create": "إنشاء مطالبة",
    "search": "بحث في المطالبات...",
    "type": "النوع",
    "author": "المؤلف",
    "views": "المشاهدات",
    "votes": "الأصوات",
    "upvote": "تصويت إيجابي",
    "downvote": "تصويت سلبي",
    "bookmark": "إضافة للمفضلة",
    "comment": "تعليق",
    "share": "مشاركة",
    "edit": "تعديل",
    "delete": "حذف",
    "copyPrompt": "نسخ المطالبة",
    "fillPlaceholders": "املأ الحقول أدناه"
  },
  "forms": {
    "email": "البريد الإلكتروني",
    "username": "اسم المستخدم",
    "password": "كلمة المرور",
    "confirmPassword": "تأكيد كلمة المرور",
    "firstName": "الاسم الأول",
    "lastName": "اسم العائلة",
    "bio": "نبذة عني",
    "submit": "إرسال",
    "cancel": "إلغاء",
    "save": "حفظ",
    "required": "هذا الحقل مطلوب"
  },
  "auth": {
    "login": "تسجيل الدخول",
    "register": "إنشاء حساب",
    "welcomeBack": "مرحباً بعودتك!",
    "newUser": "مستخدم جديد؟",
    "existingUser": "لديك حساب بالفعل؟",
    "signInHere": "سجل دخولك هنا",
    "signUpHere": "أنشئ حسابك هنا"
  },
  "theme": {
    "light": "فاتح",
    "dark": "داكن",
    "toggle": "تبديل المظهر"
  }
}
```

#### 4. i18n Configuration

**`src/i18n.js`**

```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import enTranslation from './locales/en/translation.json';
import arTranslation from './locales/ar/translation.json';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: enTranslation
      },
      ar: {
        translation: arTranslation
      }
    },
    fallbackLng: 'en',
    debug: false,
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
```

#### 5. React Components with i18n

**Language Switcher Component**

```jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    document.documentElement.dir = lng === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lng;
  };

  return (
    <div className="language-switcher">
      <button
        onClick={() => changeLanguage('en')}
        className={i18n.language === 'en' ? 'active' : ''}
      >
        English
      </button>
      <button
        onClick={() => changeLanguage('ar')}
        className={i18n.language === 'ar' ? 'active' : ''}
      >
        العربية
      </button>
    </div>
  );
}

export default LanguageSwitcher;
```

**Using Translations in Components**

```jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

function PromptCard({ prompt }) {
  const { t } = useTranslation();

  return (
    <div className="prompt-card">
      <h3>{prompt.title}</h3>
      <p>{prompt.body}</p>
      <div className="stats">
        <span>{t('prompts.views')}: {prompt.views}</span>
        <span>{t('prompts.votes')}: {prompt.vote_count}</span>
      </div>
      <div className="actions">
        <button>{t('prompts.upvote')}</button>
        <button>{t('prompts.downvote')}</button>
        <button>{t('prompts.bookmark')}</button>
      </div>
    </div>
  );
}
```

---

## Dark/Light Theme System

### 1. Theme Context

**`src/context/ThemeContext.js`**

```javascript
import React, { createContext, useState, useEffect, useContext } from 'react';

const ThemeContext = createContext();

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    // Check localStorage first
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) return savedTheme;

    // Check system preference
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  });

  useEffect(() => {
    // Apply theme to document
    document.documentElement.className = theme;
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

### 2. Theme Toggle Component

**`src/components/ThemeToggle.js`**

```jsx
import React from 'react';
import { useTheme } from '../context/ThemeContext';
import { useTranslation } from 'react-i18next';
import { Moon, Sun } from 'lucide-react'; // or any icon library

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const { t } = useTranslation();

  return (
    <button
      onClick={toggleTheme}
      className="theme-toggle"
      aria-label={t('theme.toggle')}
    >
      {theme === 'light' ? (
        <Moon className="w-5 h-5" />
      ) : (
        <Sun className="w-5 h-5" />
      )}
      <span className="ml-2">
        {theme === 'light' ? t('theme.dark') : t('theme.light')}
      </span>
    </button>
  );
}

export default ThemeToggle;
```

### 3. CSS Variables for Theming

**`src/styles/themes.css`**

```css
/* Root variables */
:root {
  /* Light theme colors */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-secondary: #64748b;
  --color-success: #10b981;
  --color-danger: #ef4444;
  --color-warning: #f59e0b;

  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  --bg-hover: #e2e8f0;

  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-tertiary: #64748b;
  --text-inverse: #ffffff;

  --border-color: #e2e8f0;
  --border-color-hover: #cbd5e1;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* Dark theme */
.dark {
  --color-primary: #60a5fa;
  --color-primary-hover: #3b82f6;
  --color-secondary: #94a3b8;
  --color-success: #34d399;
  --color-danger: #f87171;
  --color-warning: #fbbf24;

  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --bg-tertiary: #334155;
  --bg-hover: #475569;

  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-tertiary: #94a3b8;
  --text-inverse: #0f172a;

  --border-color: #334155;
  --border-color-hover: #475569;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.5);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.5);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);
}

/* Apply theme colors */
body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.card {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.button-primary {
  background-color: var(--color-primary);
  color: var(--text-inverse);
}

.button-primary:hover {
  background-color: var(--color-primary-hover);
}

/* RTL Support */
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .ml-2 { margin-left: 0; margin-right: 0.5rem; }
[dir="rtl"] .mr-2 { margin-right: 0; margin-left: 0.5rem; }
[dir="rtl"] .pl-4 { padding-left: 0; padding-right: 1rem; }
[dir="rtl"] .pr-4 { padding-right: 0; padding-left: 1rem; }
```

### 4. Tailwind CSS Dark Mode (Alternative)

**`tailwind.config.js`**

```javascript
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#3b82f6',
          dark: '#60a5fa'
        }
      }
    },
  },
  plugins: [],
}
```

**Usage in Components:**

```jsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h1 className="text-blue-600 dark:text-blue-400">Hello World</h1>
</div>
```

---

## Error Responses

All API endpoints follow consistent error response format:

### 400 Bad Request

```json
{
  "detail": "Validation error",
  "errors": {
    "email": ["This field is required."],
    "password": ["Password must be at least 8 characters."]
  }
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
  "detail": "An error occurred on the server."
}
```

---

## Complete Type Definitions (TypeScript)

**`src/types/api.ts`**

```typescript
// User Types
export interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  bio: string;
  role: 'user' | 'pro' | 'moderator' | 'admin';
  full_name: string;
  is_pro: boolean;
  is_moderator: boolean;
  date_joined: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

// Prompt Types
export interface Prompt {
  id: string;
  type: 'text' | 'image' | 'music';
  title: string;
  slug: string;
  body: string;
  context: Record<string, any> | null;
  author: {
    id: string;
    username: string;
    full_name: string;
  };
  views: number;
  vote_count: number;
  tags: string[];
  is_bookmarked: boolean;
  user_vote: 1 | -1 | null;
  created_at: string;
  updated_at: string;
}

export interface PromptCreate {
  type: 'text' | 'image' | 'music';
  title: string;
  body: string;
  context?: Record<string, any>;
  tags?: string[];
}

// Content Types
export interface Blog {
  id: string;
  title: string;
  slug: string;
  content: string;
  author: {
    id: string;
    username: string;
    full_name: string;
  };
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface News {
  id: string;
  title: string;
  slug: string;
  content: string;
  author: {
    id: string;
    username: string;
    full_name: string;
  };
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface Tool {
  id: string;
  name: string;
  slug: string;
  description: string;
  url: string;
  type: {
    id: string;
    name: string;
    description: string;
  } | null;
  author: {
    id: string;
    username: string;
    full_name: string;
  };
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface ToolType {
  id: string;
  name: string;
  description: string;
}

// Interaction Types
export interface Comment {
  id: string;
  commentable_type: 1 | 2 | 3 | 4; // 1=prompts, 2=tools, 3=news, 4=blogs
  commentable_id: string;
  author: {
    id: string;
    username: string;
    full_name: string;
  };
  body: string;
  is_edited: boolean;
  created_at: string;
  updated_at: string;
}

export interface Vote {
  votable_type: 1 | 2 | 3 | 4;
  votable_id: string;
  value: 1 | -1;
  created_at: string;
}

export interface Bookmark {
  bookmarkable_type: 1 | 2 | 3 | 4;
  bookmarkable_id: string;
  created_at: string;
}

// Tag Types
export interface Tag {
  id: string;
  name: string;
  usage_count: number;
  created_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// API Request/Response Types
export type ApiResponse<T> = {
  data: T;
  status: number;
  message?: string;
};

export type ApiError = {
  detail: string;
  errors?: Record<string, string[]>;
};
```

---

## Complete React Service Layer

**`src/services/api.service.ts`**

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';
import type { 
  User, AuthResponse, Prompt, PromptCreate, 
  Blog, News, Tool, ToolType, Comment, Vote, 
  Bookmark, Tag, PaginatedResponse 
} from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(
              `${API_BASE_URL}/auth/token/refresh/`,
              { refresh: refreshToken }
            );

            const { access } = response.data;
            localStorage.setItem('access_token', access);

            originalRequest.headers.Authorization = `Bearer ${access}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async register(data: {
    email: string;
    username: string;
    password: string;
    password_confirm: string;
    first_name?: string;
    last_name?: string;
  }): Promise<User> {
    const response = await this.api.post('/auth/register/', data);
    return response.data;
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await this.api.post('/auth/login/', { email, password });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get('/auth/me/');
    return response.data;
  }

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await this.api.patch('/auth/me/', data);
    return response.data;
  }

  // Prompts
  async getPrompts(params?: {
    type?: string;
    author__username?: string;
    search?: string;
    ordering?: string;
    page?: number;
  }): Promise<PaginatedResponse<Prompt>> {
    const response = await this.api.get('/prompts/', { params });
    return response.data;
  }

  async getPrompt(slug: string): Promise<Prompt> {
    const response = await this.api.get(`/prompts/${slug}/`);
    return response.data;
  }

  async createPrompt(data: PromptCreate): Promise<Prompt> {
    const response = await this.api.post('/prompts/', data);
    return response.data;
  }

  async updatePrompt(slug: string, data: Partial<PromptCreate>): Promise<Prompt> {
    const response = await this.api.patch(`/prompts/${slug}/`, data);
    return response.data;
  }

  async deletePrompt(slug: string): Promise<void> {
    await this.api.delete(`/prompts/${slug}/`);
  }

  async getMyPrompts(): Promise<PaginatedResponse<Prompt>> {
    const response = await this.api.get('/prompts/my_prompts/');
    return response.data;
  }

  // Blogs
  async getBlogs(params?: { search?: string; ordering?: string; page?: number }): 
    Promise<PaginatedResponse<Blog>> {
    const response = await this.api.get('/blogs/', { params });
    return response.data;
  }

  async getBlog(slug: string): Promise<Blog> {
    const response = await this.api.get(`/blogs/${slug}/`);
    return response.data;
  }

  async createBlog(data: { title: string; content: string; tags?: string[] }): 
    Promise<Blog> {
    const response = await this.api.post('/blogs/', data);
    return response.data;
  }

  async updateBlog(slug: string, data: Partial<{ title: string; content: string; tags: string[] }>): 
    Promise<Blog> {
    const response = await this.api.patch(`/blogs/${slug}/`, data);
    return response.data;
  }

  async deleteBlog(slug: string): Promise<void> {
    await this.api.delete(`/blogs/${slug}/`);
  }

  // News
  async getNews(params?: { search?: string; ordering?: string; page?: number }): 
    Promise<PaginatedResponse<News>> {
    const response = await this.api.get('/news/', { params });
    return response.data;
  }

  async getNewsItem(slug: string): Promise<News> {
    const response = await this.api.get(`/news/${slug}/`);
    return response.data;
  }

  // Tools
  async getTools(params?: { type?: string; search?: string; ordering?: string; page?: number }): 
    Promise<PaginatedResponse<Tool>> {
    const response = await this.api.get('/tools/', { params });
    return response.data;
  }

  async getTool(slug: string): Promise<Tool> {
    const response = await this.api.get(`/tools/${slug}/`);
    return response.data;
  }

  async getToolTypes(): Promise<ToolType[]> {
    const response = await this.api.get('/tool-types/');
    return response.data;
  }

  // Comments
  async getComments(commentableType: number, commentableId: string): 
    Promise<PaginatedResponse<Comment>> {
    const response = await this.api.get('/comments/', {
      params: { commentable_type: commentableType, commentable_id: commentableId }
    });
    return response.data;
  }

  async createComment(data: { 
    commentable_type: number; 
    commentable_id: string; 
    body: string 
  }): Promise<Comment> {
    const response = await this.api.post('/comments/', data);
    return response.data;
  }

  async updateComment(id: string, body: string): Promise<Comment> {
    const response = await this.api.patch(`/comments/${id}/`, { body });
    return response.data;
  }

  async deleteComment(id: string): Promise<void> {
    await this.api.delete(`/comments/${id}/`);
  }

  // Votes
  async vote(votableType: number, votableId: string, value: 1 | -1): 
    Promise<Vote> {
    const response = await this.api.post('/votes/', {
      votable_type: votableType,
      votable_id: votableId,
      value
    });
    return response.data;
  }

  async removeVote(votableType: number, votableId: string): Promise<void> {
    await this.api.delete('/votes/remove_vote/', {
      params: { votable_type: votableType, votable_id: votableId }
    });
  }

  // Bookmarks
  async getMyBookmarks(): Promise<Bookmark[]> {
    const response = await this.api.get('/bookmarks/');
    return response.data;
  }

  async addBookmark(bookmarkableType: number, bookmarkableId: string): 
    Promise<Bookmark> {
    const response = await this.api.post('/bookmarks/', {
      bookmarkable_type: bookmarkableType,
      bookmarkable_id: bookmarkableId
    });
    return response.data;
  }

  async removeBookmark(bookmarkableType: number, bookmarkableId: string): 
    Promise<void> {
    await this.api.delete('/bookmarks/remove_bookmark/', {
      params: { bookmarkable_type: bookmarkableType, bookmarkable_id: bookmarkableId }
    });
  }

  // Tags
  async getTags(params?: { search?: string; ordering?: string }): Promise<Tag[]> {
    const response = await this.api.get('/tags/', { params });
    return response.data;
  }

  async getTag(id: string): Promise<Tag> {
    const response = await this.api.get(`/tags/${id}/`);
    return response.data;
  }

  async createTag(name: string): Promise<Tag> {
    const response = await this.api.post('/tags/', { name });
    return response.data;
  }
}

export default new ApiService();
```

---

## Summary: Content Type IDs

| Content Type | ID  | Usage                            |
| ------------ | --- | -------------------------------- |
| **Prompts**  | `1` | Comments, Votes, Bookmarks, Tags |
| **Tools**    | `2` | Comments, Votes, Bookmarks, Tags |
| **News**     | `3` | Comments, Votes, Bookmarks, Tags |
| **Blogs**    | `4` | Comments, Votes, Bookmarks, Tags |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ PROMPT PLATFORM API - QUICK REFERENCE                       │
├─────────────────────────────────────────────────────────────┤
│ BASE URL: http://localhost:8000/api/                        │
├─────────────────────────────────────────────────────────────┤
│ AUTHENTICATION                                              │
│  POST /auth/register/          Register new user            │
│  POST /auth/login/             Login (get JWT)              │
│  POST /auth/token/refresh/     Refresh token                │
│  GET  /auth/me/                Get current user             │
│  PATCH /auth/me/               Update profile               │
├─────────────────────────────────────────────────────────────┤
│ PROMPTS                                                     │
│  GET    /prompts/              List all                     │
│  GET    /prompts/{slug}/       Get one                      │
│  POST   /prompts/              Create (Auth)                │
│  PATCH  /prompts/{slug}/       Update (Owner/Mod)           │
│  DELETE /prompts/{slug}/       Delete (Owner/Mod)           │
│  GET    /prompts/my_prompts/   My prompts                   │
├─────────────────────────────────────────────────────────────┤
│ CONTENT (Blogs, News, Tools)                                │
│  /blogs/, /news/, /tools/      Same CRUD as prompts         │
│  /tool-types/                  Tool categories              │
├─────────────────────────────────────────────────────────────┤
│ INTERACTIONS                                                │
│  POST   /comments/             Create comment (Auth)        │
│  POST   /votes/                Vote (Auth)                  │
│  POST   /bookmarks/            Bookmark (Auth)              │
│  DELETE /votes/remove_vote/    Remove vote                  │
│  DELETE /bookmarks/remove_bookmark/  Remove bookmark        │
├─────────────────────────────────────────────────────────────┤
│ TAGS                                                        │
│  GET  /tags/                   List all tags                │
│  POST /tags/                   Create tag (Mod)             │
│  GET  /tags/{id}/items/        Get tagged items             │
├─────────────────────────────────────────────────────────────┤
│ PLACEHOLDERS IN PROMPTS                                     │
│  Syntax: {PLACEHOLDER_NAME}                                 │
│  Example: "Write a {LENGTH} email about {TOPIC}"            │
│  Frontend: Parse and render as inline inputs                │
├─────────────────────────────────────────────────────────────┤
│ USER ROLES                                                  │
│  Anonymous → User → Pro → Moderator → Admin                 │
└─────────────────────────────────────────────────────────────┘
```

This documentation is complete and ready to hand off to your frontend team! 🚀
