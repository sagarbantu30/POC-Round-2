# Testing Guide: Parameter Verification

## Quick Start Testing

### Step 1: Monitor the Backend Logs
Open the terminal where uvicorn is running and look for the detailed logs.

### Step 2: Upload a Test Document

**Action:** Go to `http://localhost:3000/documents` → Upload a PDF

**Expected Logs:**
```
[DOCUMENT PROCESSING] Processing: test.pdf
  - document_id: 507f1f77bcf86cd799439011
  - chunk_size (from DB): 1000
  - chunk_overlap (from DB): 200
  - is_company_policy: false
  - loaded 10 pages/sections
  - created 25 chunks with chunk_size=1000, overlap=200
[DOCUMENT PROCESSING] Successfully added 25 chunks to vector store
```

**What This Tells You:**
- ✅ chunk_size of 1000 was used (from database)
- ✅ chunk_overlap of 200 was used (from database)
- ✅ Document was split into 25 chunks using these settings

---

### Step 3: Ask a Question About the Document

**Action:** Go to `http://localhost:3000/chat/document` → Select document → Ask a question

**Expected Logs:**
```
======================================================================
[CHAT REQUEST] Received query: "What is the main topic?"
======================================================================

[SETTINGS LOADED FROM DB]
  - chunk_size: 1000
  - chunk_overlap: 200
  - temperature: 0.7
  - top_p: 1.0
  - top_k: 100
  - model_name: gpt-3.5-turbo

[LLM INIT] Initializing ChatOpenAI with:
  - model_name: gpt-3.5-turbo
  - temperature: 0.7
  - top_p: 1.0
[LLM INIT] ChatOpenAI initialized successfully

[RETRIEVER] Creating retriever with:
  - top_k (num documents to retrieve): 100

[RETRIEVAL RESULTS]
  - Retrieved 100 documents with top_k=100
  - Sample metadata: {'document_id': '507f1f77bcf86cd799439011', 'filename': 'test.pdf'}
  - Sample content (first 100 chars): "Main topic content here..."

[RAG CHAIN] Building RAG chain with LLM parameters:
  - LLM Model: gpt-3.5-turbo
  - Temperature: 0.7
  - Top P: 1.0

[INVOKING RAG CHAIN] Processing query with LLM...
[RAG CHAIN] Response received (length: 342 chars)

[CHAT COMPLETE] Sources: ['test.pdf']
======================================================================
```

**What This Tells You:**
- ✅ Settings were loaded from database (not hardcoded from .env)
- ✅ LLM was initialized with correct model, temperature, and top_p
- ✅ Retriever was created with top_k=100
- ✅ 100 documents were retrieved (matching top_k)
- ✅ RAG chain used the configured LLM parameters

---

## Advanced Testing: Change Settings

### Test 1: Increase Temperature (More Creative)

**Step 1:** Go to `http://localhost:3000/settings`

**Step 2:** Change temperature from `0.7` to `0.2` (Less creative, more focused)

**Step 3:** Click "Save Settings"

**Expected:** See success message ✓

**Step 4:** Ask a question in chat

**Expected Logs:**
```
[SETTINGS LOADED FROM DB]
  - temperature: 0.2    ← Changed from 0.7!

[LLM INIT] Initializing ChatOpenAI with:
  - temperature: 0.2    ← Passed to LLM!
```

**Observation:** LLM responses should be more focused and deterministic (less random/creative)

---

### Test 2: Change Top K (Number of Retrieved Docs)

**Step 1:** Go to `http://localhost:3000/settings`

**Step 2:** Change `top_k` from `100` to `5` (Retrieve fewer documents)

**Step 3:** Click "Save Settings"

**Expected:** See success message ✓

**Step 4:** Ask a question in chat

**Expected Logs:**
```
[SETTINGS LOADED FROM DB]
  - top_k: 5    ← Changed from 100!

[RETRIEVER] Creating retriever with:
  - top_k (num documents to retrieve): 5

[RETRIEVAL RESULTS]
  - Retrieved 5 documents with top_k=5    ← Only 5 instead of 100!
```

**Observation:** Fewer documents are retrieved, may result in less comprehensive answers

---

### Test 3: Change Chunk Size (Document Splitting)

**Step 1:** Go to `http://localhost:3000/settings`

**Step 2:** Change `chunk_size` from `1000` to `500` (Smaller chunks)

**Step 3:** Click "Save Settings"

**Expected:** See success message ✓

**Step 4:** Upload a new test document

**Expected Logs:**
```
[DOCUMENT PROCESSING] Processing: new_test.pdf
  - chunk_size (from DB): 500    ← Changed from 1000!
  - chunk_overlap (from DB): 200
  - created 50 chunks with chunk_size=500, overlap=200    ← More chunks with smaller size!
```

**Observation:** More chunks are created (double the amount) because each chunk is smaller

---

### Test 4: Change Model Name

**Step 1:** Go to `http://localhost:3000/settings`

**Step 2:** Change model from `gpt-3.5-turbo` to `gpt-4` (if you have access)

**Step 3:** Click "Save Settings"

**Expected:** See success message ✓

**Step 4:** Ask a question in chat

**Expected Logs:**
```
[SETTINGS LOADED FROM DB]
  - model_name: gpt-4    ← Changed from gpt-3.5-turbo!

[LLM INIT] Initializing ChatOpenAI with:
  - model_name: gpt-4    ← Passed to LLM!
```

**Observation:** More advanced model is now used for responses

---

## Verification Checklist

### Settings Page (`/settings`)
- [ ] Page loads with current values from database
- [ ] Can change each parameter without error
- [ ] "Save Settings" button shows "Saving..." state
- [ ] Success message appears after saving
- [ ] Values persist after page refresh

### Document Upload
- [ ] Logs show `[DOCUMENT PROCESSING]` section
- [ ] chunk_size value matches database setting
- [ ] chunk_overlap value matches database setting
- [ ] Chunk count changes when you adjust chunk_size

### Chat/Question Asking
- [ ] Logs show `[SETTINGS LOADED FROM DB]` section
- [ ] All 6 parameters are listed in logs
- [ ] `[LLM INIT]` section shows correct model, temperature, top_p
- [ ] `[RETRIEVER]` section shows correct top_k
- [ ] `[RETRIEVAL RESULTS]` shows same number of docs as top_k
- [ ] LLM response quality changes when you adjust temperature/model

### Database Verification
Check MongoDB to confirm settings are stored:

```javascript
// Connect to MongoDB and run:
use rag_database
db.rag_settings.findOne()

// Should return:
{
  "_id": ObjectId("..."),
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "temperature": 0.7,
  "top_p": 1.0,
  "top_k": 100,
  "model_name": "gpt-3.5-turbo",
  "created_at": ISODate("2026-02-03T..."),
  "updated_at": ISODate("2026-02-03T...")
}
```

---

## Troubleshooting

### Settings page shows defaults but changes don't persist
**Issue:** Settings not being saved to MongoDB
**Solution:** 
1. Check MongoDB connection in logs
2. Verify `rag_settings` collection exists
3. Check browser console for API errors

### Logs show old settings after changing them
**Issue:** Database query returned cached/old data
**Solution:**
1. Verify settings were actually saved in MongoDB
2. Check `updated_at` timestamp in database
3. Clear browser cache if needed

### Logs don't show the detailed parameter information
**Issue:** Might be using an older version of RAGService
**Solution:**
1. Verify all RAG service changes were saved
2. Restart uvicorn: `uvicorn app.main:app --reload`
3. Refresh browser and try again

### Top K seems wrong (not using the value from settings)
**Issue:** top_k might be hardcoded somewhere
**Solution:**
1. Check logs for `[RETRIEVER]` section
2. Confirm it shows the correct top_k value
3. If wrong, check `RAGService.chat()` method

---

## Summary

The parameter flow is now fully traceable through logs:

1. **Settings Loaded** → `[SETTINGS LOADED FROM DB]` section shows what was fetched
2. **LLM Initialized** → `[LLM INIT]` section shows LLM is using those parameters
3. **Retriever Created** → `[RETRIEVER]` section shows retriever using top_k
4. **Documents Retrieved** → `[RETRIEVAL RESULTS]` section shows how many documents
5. **RAG Chain Invoked** → `[RAG CHAIN]` section confirms LLM parameters are active

You can now easily verify that:
- ✅ Parameters are stored in database
- ✅ Parameters are fetched from database
- ✅ Parameters are passed to the LLM
- ✅ Parameters are passed to the retriever
- ✅ Changes to settings immediately affect subsequent operations
