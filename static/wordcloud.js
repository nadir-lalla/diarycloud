  const commonWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "cannot", "could", "did", "do", "does",
    "doing", "down", "during", "each", "else", "for", "from", "further", "had", "has",
    "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "im", "if", "in", "into", "is", "it", "its", "itself", "just", "ll", "m",
    "ma", "me", "more", "most", "mr", "mrs", "ms", "my", "myself", "no", "nor", "not",
    "now", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "she", "should", "so", "some", "such",
    "than", "that", "the", "their", "theirs", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up", "very",
    "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "whose", "why", "will", "with", "would", "you", "your", "yours", "yourself", "yourselves"];

  const textContent = text_from_db
  
  const words = textContent.split(/\s+/);

  const filteredWords = words.filter(word => !commonWords.includes(word.toLowerCase()));

  function countUniqueWords(filteredWords) {
    const wordCounts = {};

    for (const word of filteredWords) {
      const uppercaseWord = word.toUpperCase();

      if (!wordCounts.hasOwnProperty(uppercaseWord)) {
        wordCounts[uppercaseWord] = 1;
      } else {
        wordCounts[uppercaseWord]++;
      }
    }

    const uniqueWords = [];
    for (const word in wordCounts) {
      uniqueWords.push([word, wordCounts[word]]);
    }
    return uniqueWords;
  }

  const uniqueWordsWithCounts = countUniqueWords(filteredWords);
  
  let maxNameValue = 0;

  uniqueWordsWithCounts.forEach((entry) => {
    maxNameValue = Math.max(maxNameValue, entry[1]);
  });
  
  const displayName = dName
  maxNameValue = maxNameValue * 1.5

  console.log(displayName, maxNameValue)

  uniqueWordsWithCounts.push([displayName, maxNameValue]);



  var options = {
    list: uniqueWordsWithCounts,
    shape: 'star',
    ellipticity: 0.85,
    fontWeight: 'normal',
    color: "random-dark",
    minFontSize: 'small',
    weightFactor: 10,
    drawOutOfBound: false,
    gridMinSize: Math.round(document.getElementById('cloud-container').clientWidth),
    gridSize: 8,
    rotateRatio: 0.5,
    backgroundColor: "white",
    fontFamily: '"Trebuchet MS","Arial Unicode MS", "Droid Fallback Sans", "sans-serif"',
    shrinkToFit: true,
    shuffle: false,
  }

  console.log(options);


  WordCloud(document.getElementById('cloud-container'), options );








