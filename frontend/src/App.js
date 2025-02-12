import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  LinearProgress, 
  Paper,
  ThemeProvider,
  createTheme,
  useMediaQuery,
  Card
} from '@mui/material';
import SentenceForm from './components/SentenceForm';
import axios from 'axios';

// Membuat tema custom
const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
  },
  components: {
    MuiContainer: {
      styleOverrides: {
        root: {
          paddingBottom: '2rem',
        },
      },
    },
  },
});

function App() {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState(null);
  const [key, setKey] = useState(0);
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const simulateProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 90) {
          clearInterval(interval);
          return 90;
        }
        return prevProgress + 10;
      });
    }, 500);

    return interval;
  };

  const handleSubmit = async (sentences) => {
    setLoading(true);
    setError(null);
    setVideoUrl(null);
    
    const progressInterval = simulateProgress();
    
    try {
      const response = await axios.post('http://localhost:5000/api/generate-video', {
        sentences
      });
      
      setProgress(100);
      setVideoUrl(`http://localhost:5000${response.data.video_url}`);
      setKey(prevKey => prevKey + 1);
    } catch (err) {
      setError(err.response?.data?.error || 'Terjadi kesalahan');
    } finally {
      clearInterval(progressInterval);
      setTimeout(() => {
        setLoading(false);
        setProgress(0);
      }, 500);
    }
  };

  useEffect(() => {
    return () => {
      setVideoUrl(null);
    };
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box sx={{ 
          minHeight: '100vh',
          py: 4,
          display: 'flex',
          flexDirection: 'column',
          gap: 4
        }}>
          <Paper 
            elevation={3}
            sx={{ 
              p: 4, 
              borderRadius: 2,
              background: 'linear-gradient(45deg, #2196f3 30%, #21cbf3 90%)',
              color: 'white'
            }}
          >
            <Typography 
              variant={isMobile ? "h5" : "h4"} 
              component="h1" 
              sx={{ 
                textAlign: 'center',
                fontWeight: 'bold',
                textShadow: '2px 2px 4px rgba(0,0,0,0.2)'
              }}
            >
              Generator Video Pembelajaran Bahasa
            </Typography>
          </Paper>

          <SentenceForm onSubmit={handleSubmit} />

          {loading && (
            <Card sx={{ p: 3, mt: 2 }}>
              <Box sx={{ width: '100%' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="textSecondary">
                    Generating Video...
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {progress}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={progress} 
                  sx={{ 
                    height: 10, 
                    borderRadius: 5,
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 5,
                    }
                  }}
                />
                <Box sx={{ mt: 1 }}>
                  <Typography variant="body2" color="textSecondary" align="center">
                    {progress < 30 ? 'Memproses teks...' :
                     progress < 60 ? 'Menghasilkan audio...' :
                     progress < 90 ? 'Menggabungkan video...' :
                     'Menyelesaikan... (mungkin ini membutuhkan waktu lebih lama)'}
                  </Typography>
                </Box>
              </Box>
            </Card>
          )}

          {error && (
            <Paper 
              elevation={3} 
              sx={{ 
                p: 2, 
                mt: 2, 
                bgcolor: '#ffebee',
                borderLeft: '4px solid #f44336'
              }}
            >
              <Typography color="error" sx={{ textAlign: 'center' }}>
                {error}
              </Typography>
            </Paper>
          )}

          {videoUrl && (
            <Card 
              elevation={3}
              sx={{ 
                mt: 4, 
                p: 3,
                borderRadius: 2,
                bgcolor: '#f5f5f5'
              }}
            >
              <Typography variant="h6" sx={{ mb: 2 }}>
                Video Preview
              </Typography>
              <Box 
                sx={{ 
                  position: 'relative',
                  paddingTop: '56.25%', // 16:9 Aspect Ratio
                  borderRadius: 1,
                  overflow: 'hidden'
                }}
              >
                <video 
                  key={key}
                  controls 
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                  autoPlay
                >
                  <source src={videoUrl} type="video/mp4" />
                  Browser Anda tidak mendukung tag video.
                </video>
              </Box>
            </Card>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
