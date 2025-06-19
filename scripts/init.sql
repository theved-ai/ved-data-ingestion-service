
-- Create raw_data table
CREATE TABLE raw_data (
  uuid UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  content TEXT DEFAULT NULL,
  source VARCHAR(100) NOT NULL,
  checksum TEXT,
  status VARCHAR(100) NOT NULL,
  metadata JSONB,
  retries int,
  is_archived BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_checksum ON raw_data(user_id, checksum);


-- Create chunked_data table
CREATE TABLE chunked_data (
  uuid UUID PRIMARY KEY,
  raw_data_id UUID REFERENCES raw_data(uuid),
  chunk_content TEXT NOT NULL,
  chunk_index INT,
  status VARCHAR(100) NOT NULL,
  checksum TEXT,
  metadata JSONB,
  retries int,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_doc_id ON chunked_data(raw_data_id);
CREATE INDEX idx_doc_id_status ON chunked_data(doc_id, status);
CREATE INDEX idx_status ON chunked_data(status);


CREATE TABLE meet_transcript_audio_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_data_id UUID NOT NULL REFERENCES raw_data(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    audio_format TEXT NOT NULL,
    audio_blob BYTEA NOT NULL,
    transcript TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);