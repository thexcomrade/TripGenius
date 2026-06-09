"use client";

interface Achievement {
    id: number;
    title: string;
    icon: string;
    description: string;
    unlocked: boolean;
}

interface TripItem {
    id: number;
    title: string;
    location: string;
    image: string;
    days: number;
}

interface ProfileGridProps {
    activeTab: string;
    achievements: Achievement[];
    totalTrips: number;
    savedTrips: number;
}

const sampleTrips: TripItem[] = [
    {
        id: 1,
        title: "Munnar Escape",
        location: "Kerala",
        days: 4,
        image:
            "https://images.unsplash.com/photo-1593693397690-362cb9666fc2"
    },

    {
        id: 2,
        title: "Dubai Adventure",
        location: "UAE",
        days: 5,
        image:
            "https://images.unsplash.com/photo-1512453979798-5ea266f8880c"
    },

    {
        id: 3,
        title: "Paris Dreams",
        location: "France",
        days: 6,
        image:
            "https://images.unsplash.com/photo-1502602898657-3e91760cbb34"
    },

    {
        id: 4,
        title: "Goa Beaches",
        location: "India",
        days: 3,
        image:
            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2"
    },

    {
        id: 5,
        title: "Kyoto Culture",
        location: "Japan",
        days: 7,
        image:
            "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e"
    },

    {
        id: 6,
        title: "Maldives Luxury",
        location: "Maldives",
        days: 5,
        image:
            "https://images.unsplash.com/photo-1573843981267-be1999ff37cd"
    }
];

export default function ProfileGrid({
    activeTab,
    achievements,
    totalTrips,
    savedTrips
}: ProfileGridProps) {
    function renderTrips() {
        return (
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(280px,1fr))",
                    gap: "24px"
                }}
            >
                {sampleTrips.map(
                    (trip) => (
                        <div
                            key={trip.id}
                            className="glass-card"
                            style={{
                                overflow:
                                    "hidden"
                            }}
                        >
                            <img
                                src={
                                    trip.image
                                }
                                alt={
                                    trip.title
                                }
                                style={{
                                    width:
                                        "100%",
                                    height:
                                        "220px",
                                    objectFit:
                                        "cover"
                                }}
                            />

                            <div
                                style={{
                                    padding:
                                        "20px"
                                }}
                            >
                                <h3
                                    style={{
                                        marginBottom:
                                            "8px"
                                    }}
                                >
                                    {
                                        trip.title
                                    }
                                </h3>

                                <p
                                    style={{
                                        color:
                                            "#CBD5E1",
                                        marginBottom:
                                            "8px"
                                    }}
                                >
                                    📍{" "}
                                    {
                                        trip.location
                                    }
                                </p>

                                <p
                                    style={{
                                        color:
                                            "#94A3B8"
                                    }}
                                >
                                    ⏳{" "}
                                    {
                                        trip.days
                                    }{" "}
                                    Days
                                </p>
                            </div>
                        </div>
                    )
                )}
            </div>
        );
    }

    function renderSavedTrips() {
        return (
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(280px,1fr))",
                    gap: "24px"
                }}
            >
                {sampleTrips
                    .slice(
                        0,
                        Math.max(
                            1,
                            savedTrips
                        )
                    )
                    .map(
                        (
                            trip
                        ) => (
                            <div
                                key={
                                    trip.id
                                }
                                className="glass-card"
                                style={{
                                    overflow:
                                        "hidden"
                                }}
                            >
                                <img
                                    src={
                                        trip.image
                                    }
                                    alt={
                                        trip.title
                                    }
                                    style={{
                                        width:
                                            "100%",
                                        height:
                                            "220px",
                                        objectFit:
                                            "cover"
                                    }}
                                />

                                <div
                                    style={{
                                        padding:
                                            "20px"
                                    }}
                                >
                                    <h3>
                                        {
                                            trip.title
                                        }
                                    </h3>

                                    <p
                                        style={{
                                            color:
                                                "#CBD5E1",
                                            marginTop:
                                                "10px"
                                        }}
                                    >
                                        ❤️
                                        Saved
                                        Destination
                                    </p>
                                </div>
                            </div>
                        )
                    )}
            </div>
        );
    }

    function renderAchievements() {
        return (
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit,minmax(250px,1fr))",
                    gap: "20px"
                }}
            >
                {achievements.map(
                    (
                        achievement
                    ) => (
                        <div
                            key={
                                achievement.id
                            }
                            className="glass-card"
                            style={{
                                padding:
                                    "25px",
                                opacity:
                                    achievement.unlocked
                                        ? 1
                                        : 0.45,
                                textAlign:
                                    "center"
                            }}
                        >
                            <div
                                style={{
                                    fontSize:
                                        "3rem",
                                    marginBottom:
                                        "15px"
                                }}
                            >
                                {
                                    achievement.icon
                                }
                            </div>

                            <h3
                                style={{
                                    marginBottom:
                                        "10px"
                                }}
                            >
                                {
                                    achievement.title
                                }
                            </h3>

                            <p
                                style={{
                                    color:
                                        "#CBD5E1"
                                }}
                            >
                                {
                                    achievement.description
                                }
                            </p>

                            <div
                                style={{
                                    marginTop:
                                        "15px"
                                }}
                            >
                                {achievement.unlocked ? (
                                    <span
                                        style={{
                                            color:
                                                "#22C55E",
                                            fontWeight:
                                                700
                                        }}
                                    >
                                        ✓
                                        Unlocked
                                    </span>
                                ) : (
                                    <span
                                        style={{
                                            color:
                                                "#94A3B8"
                                        }}
                                    >
                                        Locked
                                    </span>
                                )}
                            </div>
                        </div>
                    )
                )}
            </div>
        );
    }

    return (
        <section
            style={{
                maxWidth:
                    "1100px",
                margin:
                    "0 auto 50px auto"
            }}
        >
            <div
                style={{
                    marginBottom:
                        "25px"
                }}
            >
                <h2
                    style={{
                        fontSize:
                            "1.8rem",
                        fontWeight:
                            800
                    }}
                >
                    {activeTab ===
                        "trips" &&
                        `🗺️ My Trips (${totalTrips})`}

                    {activeTab ===
                        "saved" &&
                        `🔰 Saved Trips (${savedTrips})`}

                    {activeTab ===
                        "achievements" &&
                        "🏆 Achievements"}
                </h2>
            </div>

            {activeTab ===
                "trips" &&
                renderTrips()}

            {activeTab ===
                "saved" &&
                renderSavedTrips()}

            {activeTab ===
                "achievements" &&
                renderAchievements()}
        </section>
    );
}