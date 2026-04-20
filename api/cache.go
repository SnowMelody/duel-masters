package api

import (
	"duel-masters/game/match"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sync"

	"github.com/sirupsen/logrus"
)

// CardInfo struct is used for the card database api
type CardInfo struct {
	UUID         string   `json:"uid"`
	Name         string   `json:"name"`
	Civilization []string `json:"civilization"`
	Family       []string `json:"family"`
	ManaCost     int      `json:"manaCost"`
	Set          []string `json:"set"`
	Type         string   `json:"type"`
	Text         string   `json:"text"`
	Power        string   `json:"power"`
	Subtypes     []string `json:"subtypes"`
	Supertypes   []string `json:"supertypes"`
}

// Register holds all the card info
var register = make([]CardInfo, 0)
var mutex = &sync.Mutex{}

// CreateCardCache loads all cards and creates a cache of the static data
func CreateCardCache() {
	cardsList := readFromJson()

	for _, card := range cardsList {
		sets := make([]string, 0)
		for _, printing := range card.Printings {
			sets = append(sets, printing.Set)
		}

		for _, uuid := range card.UUID {
			entry := CardInfo{
				UUID:         uuid,
				Name:         card.Name,
				Civilization: card.Civilizations,
				ManaCost:     card.ManaCost,
				Set:          sets,
				Type:         card.Type,
				Text:         card.Text,
				Power:        card.Power,
				Subtypes:     card.Subtypes,
				Supertypes:   card.Supertypes,
				Family:       card.Subtypes,
			}

			register = append(register, entry)
			match.CreateIfNotExists(entry.UUID)
		}
	}

	logrus.Infof("Loaded %v cards into the cache", len(register))
}

// GetCache returns a copy of the cache
func GetCache() []CardInfo {
	return register
}

// CacheHas returns true if the specified uid exist in the cache
func CacheHas(uuid string) bool {

	mutex.Lock()

	defer mutex.Unlock()

	for _, c := range register {
		if c.UUID == uuid {
			return true
		}
	}

	return false

}

type CardsFromJson struct {
	Cards []CardFromJson `json:"cards"`
}

type CardFromJson struct {
	Civilizations []string            `json:"civilizations"`
	ManaCost      int                 `json:"cost"`
	Name          string              `json:"name"`
	Power         string              `json:"power"`
	Printings     []PrintingsFromJson `json:"printings"`
	Subtypes      []string            `json:"subtypes"`
	Supertypes    []string            `json:"supertypes"`
	Text          string              `json:"text"`
	Type          string              `json:"type"`
	UUID          []string            `json:"uuid"`
}

type PrintingsFromJson struct {
	Set         string `json:"set"`
	Id          string `json:"id"`
	Rarity      string `json:"rarity"`
	Flavor      string `json:"flavor"`
	Illustrator string `json:"illustrator"`
}

func readFromJson() []CardFromJson {
	jsonFileName := "DuelMastersCards.json"
	jsonFile, err := os.Open(jsonFileName)
	if err != nil {
		logrus.Error(fmt.Sprintf("Error loading %s", jsonFileName), err)
		return nil
	}
	defer jsonFile.Close()

	byteValue, _ := io.ReadAll(jsonFile)
	var cards CardsFromJson
	json.Unmarshal(byteValue, &cards)

	logrus.Infof("Loaded %v card details from %s", len(cards.Cards), jsonFileName)

	return cards.Cards
}
