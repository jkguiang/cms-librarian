for user in $(ls -d /hadoop/cms/store/user/* | awk -F'user/' '{print $2}'); do
    sh stage.sh $user
    echo "staged $user"
done
