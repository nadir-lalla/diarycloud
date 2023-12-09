  const commonWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "cannot", "could", "did", "do", "does",
    "doing", "down", "during", "each", "else", "for", "from", "further", "had", "has",
    "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "ll", "m",
    "ma", "me", "more", "most", "mr", "mrs", "ms", "my", "myself", "no", "nor", "not",
    "now", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "she", "should", "so", "some", "such",
    "than", "that", "the", "their", "theirs", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up", "very",
    "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "whose", "why", "will", "with", "would", "you", "your", "yours", "yourself", "yourselves"];

  const textContent = text_from_db
  const words = textContent.split(/\s+/);

  console.log(words)

  const filteredWords = words.filter(word => !commonWords.includes(word.toLowerCase()));

  console.log(filteredWords)



  // Function to count unique words in uppercase
  function countUniqueWords(filteredWords) {
    // Create an empty map to store word counts
    const wordCounts = {};

    // Loop through each word
    for (const word of filteredWords) {
      // Uppercasecase the word
      const uppercaseWord = word.toUpperCase();

      // Check if the word exists in the map
      if (!wordCounts.hasOwnProperty(uppercaseWord)) {
        // If not, initialize the count to 1
        wordCounts[uppercaseWord] = 1;
      } else {
        // If it exists, increment the count
        wordCounts[uppercaseWord]++;
      }
    }

    // Convert the map to a list of lists
    const uniqueWords = [];
    for (const word in wordCounts) {
      uniqueWords.push([word, wordCounts[word]]);
    }

    // Return the list of unique words and their counts
    return uniqueWords;
  }

  const uniqueWordsWithCounts = countUniqueWords(filteredWords);

  var options = {
    list: uniqueWordsWithCounts,
    shape: 'square',
    fontWeight: "bold",
    color: "random-dark",
    minFontSize: 'x-large',
    weightFactor: 20,
    drawOutOfBound: false,
    gridMinSize: Math.round(document.getElementById('cloud-container').clientWidth),
    rotateRatio: 0.5,
  }

  console.log(options);


  WordCloud(document.getElementById('cloud-container'), options );








