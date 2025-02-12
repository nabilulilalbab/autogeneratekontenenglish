import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Box, 
  Card, 
  IconButton,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  Paper,
  Tooltip
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import TranslateIcon from '@mui/icons-material/Translate';

const SentenceForm = ({ onSubmit }) => {
  const [sentences, setSentences] = useState([{
    en: '',
    id: '',
    explanation: {}
  }]);


  const handleAddSentence = () => {
    setSentences([...sentences, {
      en: '',
      id: '',
      explanation: {}
    }]);
  };

  const handleRemoveSentence = (index) => {
    setSentences(sentences.filter((_, i) => i !== index));
  };

  const handleChange = (index, field, value) => {
    const newSentences = [...sentences];
    if (field === 'en' || field === 'id') {
      newSentences[index][field] = value;
    }
    setSentences(newSentences);
  };

  const handleExplanationChange = (sentenceIndex, word, meaning) => {
    const newSentences = [...sentences];
    if (!word) return;
    
    newSentences[sentenceIndex].explanation = {
      ...newSentences[sentenceIndex].explanation,
      [word]: meaning
    };
    setSentences(newSentences);
  };

  const handleRemoveExplanation = (sentenceIndex, word) => {
    const newSentences = [...sentences];
    const newExplanation = { ...newSentences[sentenceIndex].explanation };
    delete newExplanation[word];
    newSentences[sentenceIndex].explanation = newExplanation;
    setSentences(newSentences);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(sentences);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, borderRadius: 2 }}>
      <Box component="form" onSubmit={handleSubmit}>
        {sentences.map((sentence, index) => (
          <Card 
            key={index} 
            sx={{ 
              p: 3, 
              mb: 2,
              borderRadius: 2,
              transition: 'all 0.3s ease',
              '&:hover': {
                boxShadow: 6
              }
            }}
          >
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              mb: 3 
            }}>
              <Typography 
                variant="h6" 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 1,
                  color: 'primary.main'
                }}
              >
                <TranslateIcon />
                Kalimat {index + 1}
              </Typography>
              <Tooltip title="Hapus Kalimat">
                <IconButton 
                  onClick={() => handleRemoveSentence(index)}
                  disabled={sentences.length === 1}
                  color="error"
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </Box>
            
            <TextField
              fullWidth
              label="Kalimat Bahasa Inggris"
              value={sentence.en}
              onChange={(e) => handleChange(index, 'en', e.target.value)}
              sx={{ mb: 2 }}
              variant="outlined"
            />
            
            <TextField
              fullWidth
              label="Kalimat Bahasa Indonesia"
              value={sentence.id}
              onChange={(e) => handleChange(index, 'id', e.target.value)}
              sx={{ mb: 2 }}
              variant="outlined"
            />

            <Accordion 
              sx={{ 
                '&:before': { display: 'none' },
                boxShadow: 'none',
                bgcolor: 'background.default'
              }}
            >
              <AccordionSummary 
                expandIcon={<ExpandMoreIcon />}
                sx={{ 
                  bgcolor: 'action.hover',
                  borderRadius: 1
                }}
              >
                <Typography sx={{ color: 'text.secondary' }}>
                  Penjelasan Kata (Opsional)
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Box sx={{ mb: 2 }}>
                  {Object.entries(sentence.explanation).map(([word, meaning], i) => (
                    <Box 
                      key={i} 
                      sx={{ 
                        display: 'flex', 
                        gap: 2, 
                        mb: 2,
                        alignItems: 'center'
                      }}
                    >
                      <TextField
                        label="Kata"
                        value={word}
                        onChange={(e) => {
                          const newWord = e.target.value;
                          handleRemoveExplanation(index, word);
                          handleExplanationChange(index, newWord, meaning);
                        }}
                        size="small"
                        sx={{ minWidth: 150 }}
                      />
                      <TextField
                        label="Arti"
                        value={meaning}
                        onChange={(e) => handleExplanationChange(index, word, e.target.value)}
                        size="small"
                        fullWidth
                      />
                      <Tooltip title="Hapus Penjelasan">
                        <IconButton 
                          onClick={() => handleRemoveExplanation(index, word)}
                          size="small"
                          color="error"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  ))}
                  <Button
                    startIcon={<AddIcon />}
                    onClick={() => handleExplanationChange(index, `Kata ${Object.keys(sentence.explanation).length + 1}`, '')}
                    variant="outlined"
                    size="small"
                    sx={{ mt: 1 }}
                  >
                    Tambah Penjelasan
                  </Button>
                </Box>
              </AccordionDetails>
            </Accordion>
          </Card>
        ))}
        
        <Box sx={{ 
          mt: 3, 
          display: 'flex', 
          gap: 2,
          justifyContent: 'center'
        }}>
          <Button 
            variant="outlined" 
            onClick={handleAddSentence}
            startIcon={<AddIcon />}
            sx={{ borderRadius: 2 }}
          >
            Tambah Kalimat
          </Button>
          <Button 
            variant="contained" 
            type="submit"
            sx={{ 
              borderRadius: 2,
              background: 'linear-gradient(45deg, #2196f3 30%, #21cbf3 90%)',
              color: 'white',
              boxShadow: '0 3px 5px 2px rgba(33, 203, 243, .3)'
            }}
          >
            Generate Video
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default SentenceForm; 