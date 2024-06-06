while read -r domain; do
    ranking=$(grep -i ",$domain$" tranco_LJ494.csv | cut -d',' -f1)
    if [[ -n $ranking ]]; then
        echo "Domain: $domain, Ranking: $ranking"
    else
        echo "Domain: $domain, Ranking not found"
    fi
done < domains_to_show_rankings.txt

